from fastapi.testclient import TestClient

from app.api import dashboard
from app.main import app

client = TestClient(app)


def test_dashboard_list_files(monkeypatch):
    monkeypatch.setattr(
        dashboard,
        "list_file_entries",
        lambda: [
            {
                "file_id": "file-001",
                "filename": "sample.txt",
                "uri": "file://artifacts/sample.txt",
                "content_type": "text/plain",
                "metadata": {},
            }
        ],
    )

    response = client.get("/api/files")

    assert response.status_code == 200
    body = response.json()
    assert "files" in body
    assert body["files"][0]["file_id"] == "file-001"


def test_dashboard_delete_file_is_forbidden():
    response = client.delete("/api/files/file-001")

    assert response.status_code == 403
    assert response.json()["detail"]["error"] == "delete_requires_approval"


def test_dashboard_annotate_file_success(monkeypatch):
    def fake_annotate_file_entry(file_id, payload):
        return {
            "file_id": file_id,
            "filename": "sample.txt",
            "uri": "file://artifacts/sample.txt",
            "content_type": "text/plain",
            "metadata": payload,
        }

    monkeypatch.setattr(dashboard, "annotate_file_entry", fake_annotate_file_entry)
    monkeypatch.setattr(
        dashboard,
        "append_audit_event",
        lambda **kwargs: {
            "event_type": kwargs["event_type"],
            "actor": kwargs["actor"],
            "metadata": kwargs["metadata"],
        },
    )

    response = client.post(
        "/api/files/file-001/metadata",
        headers={"x-actor": "user@example.com"},
        json={"program": "CDYP7"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["file"]["file_id"] == "file-001"
    assert body["file"]["metadata"]["program"] == "CDYP7"


def test_dashboard_annotate_missing_file_returns_404(monkeypatch):
    def fake_annotate_file_entry(file_id, payload):
        raise KeyError(file_id)

    monkeypatch.setattr(dashboard, "annotate_file_entry", fake_annotate_file_entry)

    response = client.post(
        "/api/files/missing-file/metadata",
        json={"program": "CDYP7"},
    )

    assert response.status_code == 404


def test_dashboard_audit_endpoint(monkeypatch):
    monkeypatch.setattr(
        dashboard,
        "list_audit_events",
        lambda: [
            {
                "event_type": "file.annotated",
                "actor": "user@example.com",
                "metadata": {"file_id": "file-001"},
            }
        ],
    )

    response = client.get("/api/audit")

    assert response.status_code == 200
    body = response.json()
    assert "entries" in body
    assert body["entries"][0]["event_type"] == "file.annotated"


def test_dashboard_get_task_state(monkeypatch):
    monkeypatch.setattr(
        dashboard,
        "get_task_state",
        lambda task_id: {
            "task_id": task_id,
            "status": "checkpointed",
        },
    )

    response = client.get("/api/tasks/task-001/state")

    assert response.status_code == 200
    body = response.json()
    assert body["task_id"] == "task-001"
    assert body["status"] == "checkpointed"


def test_dashboard_checkpoint_task(monkeypatch):
    monkeypatch.setattr(
        dashboard,
        "write_task_state",
        lambda task_id, payload: {
            "task_id": task_id,
            **payload,
        },
    )
    monkeypatch.setattr(
        dashboard,
        "append_audit_event",
        lambda **kwargs: {
            "event_type": kwargs["event_type"],
            "actor": kwargs["actor"],
            "metadata": kwargs["metadata"],
        },
    )

    response = client.post(
        "/api/tasks/task-001/checkpoint",
        headers={"x-actor": "user@example.com"},
        json={"status": "checkpointed", "checkpoint_id": "checkpoint-001"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["task_id"] == "task-001"
    assert body["status"] == "checkpointed"
    assert body["checkpoint_id"] == "checkpoint-001"
