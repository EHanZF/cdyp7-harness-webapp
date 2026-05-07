import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from app.core.config import ROOT

INDEX_PATH = ROOT / "artifacts" / "file_index.json"
TASKS_DIR = ROOT / "artifacts" / "tasks"


def _ensure_index():
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not INDEX_PATH.exists():
        INDEX_PATH.write_text(json.dumps({}), encoding="utf-8")


def _load_index() -> dict[str, Any]:
    _ensure_index()
    try:
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_index(idx: dict[str, Any]) -> None:
    INDEX_PATH.write_text(json.dumps(idx, indent=2), encoding="utf-8")


def add_file_entry(
    blob_uri: str,
    container: str,
    blob_name: str,
    size: int,
    filename: str,
    content_type: str,
    uploaded_by: str,
    tags: dict[str, Any],
) -> dict:
    idx = _load_index()
    file_id = str(uuid.uuid4())
    entry = {
        "id": file_id,
        "blob_uri": blob_uri,
        "container": container,
        "blob_name": blob_name,
        "size": size,
        "filename": filename,
        "content_type": content_type,
        "uploaded_by": uploaded_by,
        "uploaded_at": datetime.utcnow().isoformat() + "Z",
        "tags": tags or {},
    }
    idx[file_id] = entry
    _save_index(idx)
    return entry


def list_files() -> list[dict]:
    idx = _load_index()
    return list(idx.values())


def get_file_entry(file_id: str) -> dict:
    idx = _load_index()
    if file_id not in idx:
        raise KeyError("not_found")
    return idx[file_id]


def annotate_file_entry(file_id: str, updates: dict[str, Any]) -> dict:
    idx = _load_index()
    if file_id not in idx:
        raise KeyError("not_found")
    entry = idx[file_id]
    entry.setdefault("tags", {})
    entry["tags"].update(updates)
    entry["modified_at"] = datetime.utcnow().isoformat() + "Z"
    idx[file_id] = entry
    _save_index(idx)
    return entry


def delete_file_entry(file_id: str) -> None:
    idx = _load_index()
    if file_id in idx:
        del idx[file_id]
        _save_index(idx)


def task_state_path(task_id: str) -> Path:
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    return TASKS_DIR / f"{task_id}.json"


def write_task_state(task_id: str, payload: dict[str, Any]) -> None:
    path = task_state_path(task_id)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
