from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from app.core import tooling
from app.core.config import ROOT
from app.core.models import (
    FetchArtifactToolRequest,
    GenerateReleaseSheetToolRequest,
    ResolveReplayToolRequest,
    ToolEnvelope,
    ValidateReleaseSheetToolRequest,
    WriteReceiptToolRequest,
)

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "cdyp7-runtime-harness-tooling-api"}


@router.get("/mcp/tools/list")
def mcp_tools_list():
    return {
        "tools": [
            {
                "name": "harness.generate_release_sheet",
                "description": (
                    "Generates a System Release Sheet DOCX using explicit validated input. "
                    "Does not approve or publish releases."
                ),
            },
            {
                "name": "harness.validate_release_sheet",
                "description": "Validates a generated release sheet against schema and CAT rules.",
            },
            {
                "name": "harness.write_receipt",
                "description": "Writes an immutable receipt proving a runtime event occurred.",
            },
            {"name": "harness.fetch_artifact", "description": "Returns metadata for a controlled read-only artifact."},
            {
                "name": "harness.resolve_replay",
                "description": "Resolves a prior execution using cached artifacts and receipts. No regeneration.",
            },
        ]
    }


@router.post("/mcp/tools/call")
def mcp_tools_call(env: ToolEnvelope):
    try:
        if env.tool_name == "harness.generate_release_sheet":
            return {
                "content": tooling.generate_release_sheet(
                    GenerateReleaseSheetToolRequest(**env.arguments), env.actor or "", env.run_id
                )
            }
        if env.tool_name == "harness.validate_release_sheet":
            return {"content": tooling.validate_release_sheet(ValidateReleaseSheetToolRequest(**env.arguments))}
        if env.tool_name == "harness.write_receipt":
            return {"content": tooling.write_receipt(WriteReceiptToolRequest(**env.arguments), env.actor or "")}
        if env.tool_name == "harness.fetch_artifact":
            return {"content": tooling.fetch_artifact(FetchArtifactToolRequest(**env.arguments))}
        if env.tool_name == "harness.resolve_replay":
            return {"content": tooling.resolve_replay(ResolveReplayToolRequest(**env.arguments))}
        raise ValueError("unknown_tool")
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail={"error": "tool_call_failed", "message": str(exc), "fail_closed": True}
        ) from exc


@router.post("/tools/generate-release-sheet")
def generate_release_sheet(payload: GenerateReleaseSheetToolRequest, request: Request):
    actor = request.headers.get("x-actor", "tooling.user@example.com")
    try:
        return tooling.generate_release_sheet(payload, actor, request.headers.get("x-run-id"))
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail={"error": "generate_release_sheet_failed", "message": str(exc), "fail_closed": True}
        ) from exc


@router.post("/tools/validate-release-sheet")
def validate_release_sheet(payload: ValidateReleaseSheetToolRequest):
    try:
        return tooling.validate_release_sheet(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail={"error": "validate_release_sheet_failed", "message": str(exc), "fail_closed": True}
        ) from exc


@router.post("/tools/write-receipt")
def write_receipt(payload: WriteReceiptToolRequest, request: Request):
    try:
        return tooling.write_receipt(payload, request.headers.get("x-actor", payload.actor))
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail={"error": "write_receipt_failed", "message": str(exc), "fail_closed": True}
        ) from exc


@router.post("/tools/fetch-artifact")
def fetch_artifact(payload: FetchArtifactToolRequest):
    try:
        return tooling.fetch_artifact(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=404, detail={"error": "fetch_artifact_failed", "message": str(exc), "fail_closed": True}
        )


@router.post("/tools/resolve-replay")
def resolve_replay(payload: ResolveReplayToolRequest):
    return tooling.resolve_replay(payload)


@router.get("/outputs/{filename}")
def get_local_output(filename: str):
    path = ROOT / "artifacts" / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="not_found")
    return FileResponse(
        path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=filename
    )
