import uuid
from typing import Any

from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse

from app.core.config import settings, ROOT
from app.core.storage import blob_store
from app.core.file_index import (
    add_file_entry,
    get_file_entry,
    annotate_file_entry,
    write_task_state,
    get_task_state,
    list_file_entries,
)
from app.core.ingest import start_ingest_job, get_ingest_job
from app.core.alm import list_alm_artifacts, perform_alm_action
from app.core.audit import append_audit_event, list_audit_events
from app.core.search import search as core_search, search_with_filters


def get_router() -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.post("/files/upload")
    async def upload_file(request: Request, file: UploadFile = File(...), task_id: str | None = None):
        actor = request.headers.get("x-actor", "anonymous")
        container = settings.artifacts_container
        data = await file.read()
        blob_name = f"{uuid.uuid4()}-{file.filename}"
        stored = blob_store.upload_bytes(
            container,
            blob_name,
            data,
            overwrite=False,
            content_type=file.content_type,
        )

        entry = add_file_entry(
            blob_uri=stored.blob_uri,
            container=container,
            blob_name=stored.blob_name,
            size=stored.size,
            filename=str(file.filename),
            content_type=str(file.content_type or ""),
            uploaded_by=actor,
            tags={},
        )

        append_audit_event(
            event_type="file.upload",
            actor=actor,
            metadata={"file_id": entry.get("id"), "filename": str(file.filename), "task_id": task_id},
        )
        return {"status": "ok", "file": entry}

    @router.get("/files")
    def files_list():
        return {"files": list_file_entries()}

    @router.get("/files/{file_id}")
    def files_get(file_id: str):
        try:
            entry = get_file_entry(file_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="not_found")

        uri = entry.get("blob_uri")

        if isinstance(uri, str) and uri.startswith("file://"):
            _, path = uri.split("file://", 1)
            local = ROOT / path
            if not local.exists():
                raise HTTPException(status_code=404, detail="not_found")
            return FileResponse(local, filename=entry.get("filename"))

        return {"file": entry, "url": uri}

    @router.delete("/files/{file_id}")
    def files_delete(file_id: str):
        raise HTTPException(status_code=403, detail={"error": "delete_requires_approval"})

    @router.post("/files/{file_id}/metadata")
    def files_annotate(file_id: str, payload: dict[str, Any], request: Request):
        actor = request.headers.get("x-actor", "anonymous")
        try:
            entry = annotate_file_entry(file_id, payload)
        except KeyError:
            raise HTTPException(status_code=404, detail="not_found")

        append_audit_event(
            event_type="file.annotate",
            actor=actor,
            metadata={"file_id": file_id, "updates": payload},
        )
        return {"status": "ok", "file": entry}

    @router.post("/ingest")
    def ingest_start(payload: dict[str, Any], request: Request):
        actor = request.headers.get("x-actor", "anonymous")
        file_ids = payload.get("file_ids", [])
        job_id = start_ingest_job(file_ids, actor)

        append_audit_event(
            event_type="ingest.start",
            actor=actor,
            metadata={"job_id": job_id, "file_count": len(file_ids)},
        )
        return {"job_id": job_id}

    @router.get("/ingest/{job_id}/status")
    def ingest_status(job_id: str):
        job = get_ingest_job(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="not_found")
        return {"job": job}

    @router.get("/alm/files")
    def alm_files():
        return {"files": []}

    @router.get("/alm/{system}/{artifact_type}")
    def alm_list(system: str, artifact_type: str):
        return {"artifacts": list_alm_artifacts(system, artifact_type)}

    @router.post("/alm/{system}/{artifact}/action")
    def alm_action(system: str, artifact: str, payload: dict[str, Any], request: Request):
        actor = request.headers.get("x-actor", "anonymous")
        correlation = request.headers.get("x-run-id") or str(uuid.uuid4())

        result = perform_alm_action(
            system,
            artifact,
            payload.get("action"),
            payload.get("arguments", {}),
            actor,
            correlation,
        )

        append_audit_event(
            event_type="alm.action",
            actor=actor,
            metadata={
                "system": system,
                "artifact": artifact,
                "action": payload.get("action"),
            },
        )
        return {"result": result}

    @router.get("/audit")
    def audit_list(limit: int = 200):
        return {"entries": list_audit_events()}

    @router.get("/audit/{correlation_id}")
    def audit_query(correlation_id: str):
        entries = [e for e in list_audit_events() if e.get("correlation_id") == correlation_id]
        return {"entries": entries}

    @router.get("/tasks/{task_id}/state")
    def task_state(task_id: str):
        try:
            state = get_task_state(task_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="not_found")
        return state

    @router.post("/tasks/{task_id}/checkpoint")
    def task_checkpoint(task_id: str, payload: dict[str, Any], request: Request):
        actor = request.headers.get("x-actor", "anonymous")
        state = write_task_state(task_id, payload)

        append_audit_event(
            event_type="task.checkpoint",
            actor=actor,
            metadata={"task_id": task_id, "payload": {"size": len(str(payload))}},
        )
        return state

    @router.post("/tasks/{task_id}/rest-point")
    def task_restpoint(task_id: str, payload: dict[str, Any], request: Request):
        actor = request.headers.get("x-actor", "anonymous")
        write_task_state(task_id, payload)

        append_audit_event(
            event_type="task.rest_point",
            actor=actor,
            metadata={"task_id": task_id},
        )
        return {"status": "ok"}

    @router.get("/search")
    def api_search(q: str | None = None, limit: int = 5):
        if not q or not q.strip():
            raise HTTPException(status_code=400, detail={"error": "query_required"})

        try:
            results = core_search(q, limit=limit)
        except Exception as exc:
            raise HTTPException(status_code=500, detail={"error": "search_failed", "message": str(exc)})

        return {"query": q, "results": results}

    @router.post("/search")
    def api_search_post(payload: dict[str, Any]):
        q = payload.get("query")
        limit = int(payload.get("limit", 5))
        filters = payload.get("filters")

        if not q or not str(q).strip():
            raise HTTPException(status_code=400, detail={"error": "query_required"})

        try:
            results = search_with_filters(str(q), limit=limit, filters=filters)
        except Exception as exc:
            raise HTTPException(status_code=500, detail={"error": "search_failed", "message": str(exc)})

        return {"query": q, "results": results}

    return router
