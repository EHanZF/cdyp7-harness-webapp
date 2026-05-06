<<<<<<< HEAD
from app.core.authz import require_actor
from app.core.config import settings
from app.core.models import (
    CreateReleaseSheetRequest,
    FetchArtifactToolRequest,
    GenerateReleaseSheetToolRequest,
    ResolveReplayToolRequest,
    ValidateReleaseSheetToolRequest,
    WriteReceiptToolRequest,
)
from app.core.receipts import append_receipt
from app.core.release_sheet_renderer import render_release_sheet_docx
from app.core.release_sheet_validator import validate_release_sheet_docx_blob

RUN_INDEX: dict[str, list[str]] = {}


def request_from_fields(tool_req: GenerateReleaseSheetToolRequest, actor: str) -> CreateReleaseSheetRequest:
    fields = dict(tool_req.fields)
    if "actor" not in fields:
        fields["actor"] = actor
    return CreateReleaseSheetRequest(**fields)


def generate_release_sheet(tool_req: GenerateReleaseSheetToolRequest, actor: str, run_id: str | None = None) -> dict:
    require_actor(actor)
    req = request_from_fields(tool_req, actor)
    if req.release.cat_level == "CAT5":
        if req.release_documentation.safety_case is None:
            raise ValueError("cat5_safety_case_required")
        if req.release_documentation.test_summary_report is None:
            raise ValueError("cat5_test_summary_report_required")
    result = render_release_sheet_docx(req)
    if not result.ok:
        raise RuntimeError(result.error or "render failed")
    if run_id:
        RUN_INDEX.setdefault(run_id, []).append(result.artifact_id)
    return {
        "artifact_id": result.artifact_id,
        "blob_uri": result.blob_uri,
        "sha256": result.sha256,
        "blob_name": result.blob_name,
    }


def validate_release_sheet(tool_req: ValidateReleaseSheetToolRequest) -> dict:
    # artifact_id format is srs-artifact-S011-CAT5, blob filename is tracked by delivery/CAT in this local adapter.
    parts = tool_req.artifact_id.split("-")
    delivery, cat = parts[-2], parts[-1]
    [p for p in [""]]
    # use simple deterministic filename search only in local mode
    import glob
    import os

    if settings.storage_account_url:
        raise ValueError(
            "For Azure validation, pass generated blob_name through orchestrator "
            "metadata or call create endpoint directly"
        )
    matches = glob.glob(f"artifacts/*{delivery}_{cat}.docx")
    if not matches:
        raise FileNotFoundError("artifact_not_found")
=======
from app.core.models import *
from app.core.authz import require_actor
from app.core.release_sheet_renderer import render_release_sheet_docx
from app.core.release_sheet_validator import validate_release_sheet_docx_blob
from app.core.receipts import append_receipt
from app.core.storage import blob_store
from app.core.config import settings

RUN_INDEX: dict[str, list[str]] = {}

def request_from_fields(tool_req: GenerateReleaseSheetToolRequest, actor: str) -> CreateReleaseSheetRequest:
    fields = dict(tool_req.fields)
    if 'actor' not in fields: fields['actor'] = actor
    return CreateReleaseSheetRequest(**fields)

def generate_release_sheet(tool_req: GenerateReleaseSheetToolRequest, actor: str, run_id: str | None = None) -> dict:
    require_actor(actor)
    req = request_from_fields(tool_req, actor)
    if req.release.cat_level == 'CAT5':
        if req.release_documentation.safety_case is None:
            raise ValueError('cat5_safety_case_required')
        if req.release_documentation.test_summary_report is None:
            raise ValueError('cat5_test_summary_report_required')
    result = render_release_sheet_docx(req)
    if not result.ok:
        raise RuntimeError(result.error or 'render failed')
    if run_id:
        RUN_INDEX.setdefault(run_id, []).append(result.artifact_id)
    return {'artifact_id': result.artifact_id, 'blob_uri': result.blob_uri, 'sha256': result.sha256, 'blob_name': result.blob_name}

def validate_release_sheet(tool_req: ValidateReleaseSheetToolRequest) -> dict:
    # artifact_id format is srs-artifact-S011-CAT5, blob filename is tracked by delivery/CAT in this local adapter.
    parts = tool_req.artifact_id.split('-')
    delivery, cat = parts[-2], parts[-1]
    candidates = [p for p in ['']]
    # use simple deterministic filename search only in local mode
    import glob, os
    if settings.storage_account_url:
        raise ValueError('For Azure validation, pass generated blob_name through orchestrator metadata or call create endpoint directly')
    matches = glob.glob(f'artifacts/*{delivery}_{cat}.docx')
    if not matches:
        raise FileNotFoundError('artifact_not_found')
>>>>>>> b0f8b70 (Add tooling API contract tests and validation output)
    blob_name = os.path.basename(matches[0])
    result = validate_release_sheet_docx_blob(blob_name, tool_req.validation_profile)
    return result.model_dump()

<<<<<<< HEAD

def write_receipt(tool_req: WriteReceiptToolRequest, actor: str) -> dict:
    require_actor(actor or tool_req.actor)
    return append_receipt(
        tool_req.event_type,
        actor or tool_req.actor,
        artifact_id=tool_req.artifact_id,
        artifact_sha256=tool_req.sha256,
        metadata=tool_req.metadata,
    )


def fetch_artifact(tool_req: FetchArtifactToolRequest) -> dict:
    import glob
    import os

    if settings.storage_account_url:
        raise ValueError("Azure fetch requires blob index implementation in production binding")
    matches = glob.glob("artifacts/*")
    for m in matches:
        if tool_req.artifact_id.split("-")[-2] in m and tool_req.artifact_id.split("-")[-1] in m:
            data = open(m, "rb").read()
            from app.core.hashing import sha256_bytes

            return {"blob_uri": "file://" + m, "sha256": sha256_bytes(data), "blob_name": os.path.basename(m)}
    raise FileNotFoundError("artifact_not_found")


def resolve_replay(tool_req: ResolveReplayToolRequest) -> dict:
    if tool_req.adapter_version != "v1.0.0":
        return {"status": "denied", "artifacts": [], "reason": "adapter_version_mismatch"}
    artifacts = RUN_INDEX.get(tool_req.run_id, [])
    if not artifacts:
        return {"status": "denied", "artifacts": [], "reason": "cache_miss"}
    return {"status": "resolved", "artifacts": artifacts}
=======
def write_receipt(tool_req: WriteReceiptToolRequest, actor: str) -> dict:
    require_actor(actor or tool_req.actor)
    return append_receipt(tool_req.event_type, actor or tool_req.actor, artifact_id=tool_req.artifact_id, artifact_sha256=tool_req.sha256, metadata=tool_req.metadata)

def fetch_artifact(tool_req: FetchArtifactToolRequest) -> dict:
    import glob, os
    if settings.storage_account_url:
        raise ValueError('Azure fetch requires blob index implementation in production binding')
    matches = glob.glob(f'artifacts/*')
    for m in matches:
        if tool_req.artifact_id.split('-')[-2] in m and tool_req.artifact_id.split('-')[-1] in m:
            data = open(m,'rb').read()
            from app.core.hashing import sha256_bytes
            return {'blob_uri': 'file://' + m, 'sha256': sha256_bytes(data), 'blob_name': os.path.basename(m)}
    raise FileNotFoundError('artifact_not_found')

def resolve_replay(tool_req: ResolveReplayToolRequest) -> dict:
    if tool_req.adapter_version != 'v1.0.0':
        return {'status':'denied','artifacts':[],'reason':'adapter_version_mismatch'}
    artifacts = RUN_INDEX.get(tool_req.run_id, [])
    if not artifacts:
        return {'status':'denied','artifacts':[],'reason':'cache_miss'}
    return {'status':'resolved','artifacts':artifacts}
>>>>>>> b0f8b70 (Add tooling API contract tests and validation output)
