import json

from app.core import audit


def test_list_audit_events_returns_empty_when_missing(monkeypatch, tmp_path):
    audit_path = tmp_path / "audit.jsonl"
    monkeypatch.setattr(audit, "AUDIT_LOG_PATH", audit_path, raising=False)

    assert audit.list_audit_events() == []


def test_append_audit_event_persists_event(monkeypatch, tmp_path):
    audit_path = tmp_path / "audit.jsonl"
    monkeypatch.setattr(audit, "AUDIT_LOG_PATH", audit_path, raising=False)

    event = audit.append_audit_event(
        event_type="file.annotated",
        actor="user@example.com",
        metadata={"file_id": "file-001"},
    )

    assert event["event_type"] == "file.annotated"
    assert event["actor"] == "user@example.com"
    assert event["metadata"]["file_id"] == "file-001"

    events = audit.list_audit_events()
    assert len(events) == 1
    assert events[0]["event_type"] == "file.annotated"


def test_list_audit_events_ignores_blank_lines(monkeypatch, tmp_path):
    audit_path = tmp_path / "audit.jsonl"
    audit_path.write_text(
        "\n"
        + json.dumps(
            {
                "event_type": "system.started",
                "actor": "system",
                "metadata": {},
            }
        )
        + "\n\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(audit, "AUDIT_LOG_PATH", audit_path, raising=False)

    events = audit.list_audit_events()

    assert len(events) == 1
    assert events[0]["event_type"] == "system.started"


def test_append_audit_event_creates_parent_directory(monkeypatch, tmp_path):
    audit_path = tmp_path / "nested" / "audit.jsonl"
    monkeypatch.setattr(audit, "AUDIT_LOG_PATH", audit_path, raising=False)

    audit.append_audit_event(
        event_type="test.event",
        actor="user@example.com",
        metadata={},
    )

    assert audit_path.exists()
