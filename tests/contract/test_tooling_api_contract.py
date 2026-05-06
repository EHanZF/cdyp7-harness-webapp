import json
from pathlib import Path

from app.core.models import (
    FetchArtifactToolRequest,
    GenerateReleaseSheetToolRequest,
    ResolveReplayToolRequest,
    ToolEnvelope,
    ValidateReleaseSheetToolRequest,
    WriteReceiptToolRequest,
)


def load_generate_release_sheet_tool_call() -> dict:
    root = Path(__file__).resolve().parents[2]
    tool_call_path = root / "examples" / "generate-release-sheet.tool-call.json"
    return json.loads(tool_call_path.read_text())


def test_generate_release_sheet_tool_call_contract_loads():
    call = load_generate_release_sheet_tool_call()

    envelope = ToolEnvelope(**call)
    request = GenerateReleaseSheetToolRequest(**call["arguments"])

    assert envelope.tool_name == "harness.generate_release_sheet"
    assert request.fields is not None


def test_validate_release_sheet_tool_request_contract_loads():
    request = ValidateReleaseSheetToolRequest(
        artifact_id="srs-artifact-S011-CAT5",
        validation_profile="system_release_sheet_cat5",
    )

    assert request.artifact_id == "srs-artifact-S011-CAT5"
    assert request.validation_profile == "system_release_sheet_cat5"


def test_write_receipt_tool_request_contract_loads():
    request = WriteReceiptToolRequest(
        event_type="x",
        actor="user@example.com",
        artifact_id="a",
        sha256="sha256:" + "a" * 64,
    )

    assert request.event_type == "x"
    assert request.actor == "user@example.com"
    assert request.artifact_id == "a"
    assert str(request.sha256).startswith("sha256:")


def test_fetch_artifact_tool_request_contract_loads():
    request = FetchArtifactToolRequest(
        artifact_id="srs-artifact-S011-CAT5",
    )

    assert request.artifact_id == "srs-artifact-S011-CAT5"


def test_resolve_replay_tool_request_contract_loads():
    request = ResolveReplayToolRequest(
        run_id="run-local-001",
        adapter_version="v1.0.0",
    )

    assert request.run_id == "run-local-001"
    assert request.adapter_version == "v1.0.0"
