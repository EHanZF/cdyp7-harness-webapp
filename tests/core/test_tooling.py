import pytest

from app.core import tooling
from app.core.models import (
    ResolveReplayToolRequest,
    FetchArtifactToolRequest,
    ValidateReleaseSheetToolRequest,
    WriteReceiptToolRequest,
)

from app.core import tooling
from app.core.models import ResolveReplayToolRequest

def test_resolve_replay_denies_adapter_mismatch():
    request = ResolveReplayToolRequest(
        run_id="run-local-001",
        adapter_version="bad-version",
    )

    result = tooling.resolve_replay(request)

    assert result["status"] == "denied"
    assert result["reason"] == "adapter_version_mismatch"

def test_resolve_replay_denies_cache_miss():
    request = ResolveReplayToolRequest(
        run_id="missing-run",
        adapter_version="v1.0.0",
    )

    result = tooling.resolve_replay(request)

    assert result["status"] == "denied"
    assert result["reason"] == "cache_miss"

def test_resolve_replay_returns_cached_artifacts(monkeypatch):
    monkeypatch.setitem(tooling.RUN_INDEX, "run-123", ["artifact-1"])

    request = ResolveReplayToolRequest(
        run_id="run-123",
        adapter_version="v1.0.0",
    )

    result = tooling.resolve_replay(request)

    assert result == {
        "status": "resolved",
        "artifacts": ["artifact-1"],
    }

def test_write_receipt_calls_append_receipt(monkeypatch):
    captured = {}

    def fake_append_receipt(event_type, actor, artifact_id=None, artifact_sha256=None, metadata=None):
        captured["event_type"] = event_type
        captured["actor"] = actor
        captured["artifact_id"] = artifact_id
        captured["artifact_sha256"] = artifact_sha256
        captured["metadata"] = metadata
        return {
            "event_type": event_type,
            "actor": actor,
            "artifact_id": artifact_id,
            "artifact_sha256": artifact_sha256,
            "metadata": metadata,
        }

    monkeypatch.setattr(tooling, "append_receipt", fake_append_receipt)

    request = WriteReceiptToolRequest(
        event_type="release.generated",
        actor="payload@example.com",
        artifact_id="artifact-001",
        sha256="sha256:" + "a" * 64,
        metadata={"program": "CDYP7"},
    )

    result = tooling.write_receipt(request, actor="user@example.com")

    assert result["event_type"] == "release.generated"
    assert result["actor"] == "user@example.com"
    assert result["artifact_id"] == "artifact-001"
    assert result["artifact_sha256"] == "sha256:" + "a" * 64
    assert result["metadata"]["program"] == "CDYP7"
    assert captured["actor"] == "user@example.com"


def test_write_receipt_rejects_missing_actor():
    request = WriteReceiptToolRequest(
        event_type="release.generated",
        actor="",
        artifact_id="artifact-001",
        sha256="sha256:" + "a" * 64,
        metadata={},
    )

    with pytest.raises(PermissionError):
        tooling.write_receipt(request, actor="")


def test_fetch_artifact_missing_file_raises(monkeypatch):
    import glob

    monkeypatch.setattr(glob, "glob", lambda pattern: [])

    request = FetchArtifactToolRequest(
        artifact_id="srs-artifact-S011-CAT5",
    )

    with pytest.raises(FileNotFoundError):
        tooling.fetch_artifact(request)


def test_fetch_artifact_returns_local_metadata(monkeypatch, tmp_path):
    import glob

    artifact_path = tmp_path / "release_S011_CAT5.docx"
    artifact_path.write_bytes(b"test artifact bytes")

    monkeypatch.setattr(glob, "glob", lambda pattern: [str(artifact_path)])

    request = FetchArtifactToolRequest(
        artifact_id="srs-artifact-S011-CAT5",
    )

    result = tooling.fetch_artifact(request)

    assert result["blob_uri"] == "file://" + str(artifact_path)
    assert result["blob_name"] == artifact_path.name
    assert result["sha256"].startswith("sha256:")


def test_validate_release_sheet_missing_artifact_raises(monkeypatch):
    import glob

    monkeypatch.setattr(glob, "glob", lambda pattern: [])

    request = ValidateReleaseSheetToolRequest(
        artifact_id="srs-artifact-S011-CAT5",
        validation_profile="system_release_sheet_cat5",
    )

    with pytest.raises(FileNotFoundError):
        tooling.validate_release_sheet(request)


def test_validate_release_sheet_calls_validator(monkeypatch):
    import glob

    class FakeValidationResult:
        def model_dump(self):
            return {
                "ok": True,
                "errors": [],
            }

    monkeypatch.setattr(glob, "glob", lambda pattern: ["artifacts/release_S011_CAT5.docx"])
    monkeypatch.setattr(
        tooling,
        "validate_release_sheet_docx_blob",
        lambda blob_name, validation_profile: FakeValidationResult(),
    )

    request = ValidateReleaseSheetToolRequest(
        artifact_id="srs-artifact-S011-CAT5",
        validation_profile="system_release_sheet_cat5",
    )

    result = tooling.validate_release_sheet(request)

    assert result["ok"] is True
    assert result["errors"] == []