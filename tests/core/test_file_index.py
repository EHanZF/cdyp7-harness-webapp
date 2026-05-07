import json

import pytest

from app.core import file_index


def test_file_index_starts_empty_when_index_missing(monkeypatch, tmp_path):
    index_path = tmp_path / "files.json"
    monkeypatch.setattr(file_index, "FILE_INDEX_PATH", index_path, raising=False)

    assert file_index.list_file_entries() == []


def test_register_file_entry_persists_entry(monkeypatch, tmp_path):
    index_path = tmp_path / "files.json"
    monkeypatch.setattr(file_index, "FILE_INDEX_PATH", index_path, raising=False)

    entry = file_index.register_file_entry(
        file_id="file-001",
        filename="sample.txt",
        uri="file://artifacts/sample.txt",
        content_type="text/plain",
        metadata={"program": "CDYP7"},
    )

    assert entry["file_id"] == "file-001"
    assert entry["filename"] == "sample.txt"
    assert entry["uri"] == "file://artifacts/sample.txt"

    entries = file_index.list_file_entries()
    assert len(entries) == 1
    assert entries[0]["file_id"] == "file-001"


def test_get_file_entry_returns_existing_entry(monkeypatch, tmp_path):
    index_path = tmp_path / "files.json"
    index_path.write_text(
        json.dumps(
            {
                "files": [
                    {
                        "file_id": "file-001",
                        "filename": "sample.txt",
                        "uri": "file://artifacts/sample.txt",
                        "content_type": "text/plain",
                        "metadata": {},
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(file_index, "FILE_INDEX_PATH", index_path, raising=False)

    entry = file_index.get_file_entry("file-001")

    assert entry["file_id"] == "file-001"
    assert entry["filename"] == "sample.txt"


def test_get_file_entry_raises_for_missing_entry(monkeypatch, tmp_path):
    index_path = tmp_path / "files.json"
    index_path.write_text(json.dumps({"files": []}), encoding="utf-8")
    monkeypatch.setattr(file_index, "FILE_INDEX_PATH", index_path, raising=False)

    with pytest.raises(KeyError):
        file_index.get_file_entry("missing-file")


def test_annotate_file_entry_updates_metadata(monkeypatch, tmp_path):
    index_path = tmp_path / "files.json"
    index_path.write_text(
        json.dumps(
            {
                "files": [
                    {
                        "file_id": "file-001",
                        "filename": "sample.txt",
                        "uri": "file://artifacts/sample.txt",
                        "content_type": "text/plain",
                        "metadata": {},
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(file_index, "FILE_INDEX_PATH", index_path, raising=False)

    updated = file_index.annotate_file_entry(
        "file-001",
        {
            "program": "CDYP7",
            "artifact_type": "release_sheet",
        },
    )

    assert updated["tags"]["program"] == "CDYP7"
    assert updated["tags"]["artifact_type"] == "release_sheet"

    persisted = file_index.get_file_entry("file-001")
    assert persisted["tags"]["program"] == "CDYP7"


def test_task_state_defaults_when_missing(monkeypatch, tmp_path):
    task_state_path = tmp_path / "task_state.json"
    monkeypatch.setattr(file_index, "TASK_STATE_PATH", task_state_path, raising=False)

    state = file_index.get_task_state("task-001")

    assert state["task_id"] == "task-001"
    assert state["status"] in {"new", "unknown", "not_found", "pending"}


def test_write_and_read_task_state(monkeypatch, tmp_path):
    task_state_path = tmp_path / "task_state.json"
    monkeypatch.setattr(file_index, "TASK_STATE_PATH", task_state_path, raising=False)

    written = file_index.write_task_state(
        "task-001",
        {
            "status": "checkpointed",
            "checkpoint_id": "checkpoint-001",
        },
    )

    assert written["task_id"] == "task-001"
    assert written["status"] == "checkpointed"

    read_back = file_index.get_task_state("task-001")
    assert read_back["status"] == "checkpointed"
    assert read_back["checkpoint_id"] == "checkpoint-001"
