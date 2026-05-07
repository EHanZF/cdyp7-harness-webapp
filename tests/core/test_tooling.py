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
