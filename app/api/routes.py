from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from pathlib import Path

from app.core import tooling
from app.core.config import ROOT
from app.core.models import (
    FetchArtifactToolRequest,
    GenerateReleaseSheetToolRequest,
    ResolveReplayToolRequest,
    ValidateReleaseSheetToolRequest,
    WriteReceiptToolRequest,
)

router = APIRouter()


# ✅ Health check
@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "cdyp7-runtime-harness-tooling-api",
    }


# ✅ Generate release sheet
@router.post("/tools/generate-release-sheet")
def generate_release_sheet(
    payload: GenerateReleaseSheetToolRequest,
    request: Request,
):
    actor = request.headers.get("x-actor", "tooling.user@example.com")
    run_id = request.headers.get("x-run-id")

    try:
        return tooling.generate_release_sheet(payload, actor, run_id)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "generate_release_sheet_failed",
                "message": str(exc),
                "fail_closed": True,
            },
        ) from exc


# ✅ Validate release sheet
@router.post("/tools/validate-release-sheet")
def validate_release_sheet(payload: ValidateReleaseSheetToolRequest):
    try:
        return tooling.validate_release_sheet(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "validate_release_sheet_failed",
                "message": str(exc),
                "fail_closed": True,
            },
        ) from exc


# ✅ Write receipt
@router.post("/tools/write-receipt")
def write_receipt(payload: WriteReceiptToolRequest, request: Request):
    try:
        actor = request.headers.get("x-actor", payload.actor)
        return tooling.write_receipt(payload, actor)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "write_receipt_failed",
                "message": str(exc),
                "fail_closed": True,
            },
        ) from exc


# ✅ Fetch artifact
@router.post("/tools/fetch-artifact")
def fetch_artifact(payload: FetchArtifactToolRequest):
    try:
        return tooling.fetch_artifact(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "fetch_artifact_failed",
                "message": str(exc),
                "fail_closed": True,
            },
        )

# ✅ Resolve replay
@router.post("/tools/resolve-replay")
def resolve_replay(payload: ResolveReplayToolRequest):
    try:
        return tooling.resolve_replay(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "resolve_replay_failed",
                "message": str(exc),
                "fail_closed": True,
            },
        ) from exc


# ✅ Download generated DOCX artifact
@router.get("/outputs/{filename}")
def get_local_output(filename: str):
    path = ROOT / "artifacts" / filename

    if not path.exists():
        raise HTTPException(status_code=404, detail="not_found")

    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename,
    )
