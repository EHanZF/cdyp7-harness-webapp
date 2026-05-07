import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from app.core.config import ROOT

FILE_INDEX_PATH = ROOT / "artifacts" / "file_index.json"
# optional test hook: when set to a Path, task state is written to a single file
TASK_STATE_PATH = None
TASKS_DIR = ROOT / "artifacts" / "tasks"

# backwards-compat alias
INDEX_PATH = FILE_INDEX_PATH


def _ensure_index():
    FILE_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not FILE_INDEX_PATH.exists():
        FILE_INDEX_PATH.write_text(json.dumps({}), encoding="utf-8")


def _load_index() -> dict[str, Any]:
    _ensure_index()
    try:
        raw = json.loads(FILE_INDEX_PATH.read_text(encoding="utf-8"))
        # support legacy test shape: {"files": [ {file_id, filename, uri, content_type, metadata}, ... ]}
        if isinstance(raw, dict) and "files" in raw and isinstance(raw.get("files"), list):
            out: dict[str, Any] = {}
            for e in raw.get("files", []):
                fid = e.get("file_id") or e.get("id")
                if not fid:
                    continue
                out[fid] = {
                    "id": fid,
                    "blob_uri": e.get("uri") or e.get("blob_uri", ""),
                    "container": e.get("container", ""),
                    "blob_name": e.get("blob_name") or e.get("filename", ""),
                    "size": e.get("size", 0),
                    "filename": e.get("filename"),
                    "content_type": e.get("content_type"),
                    "uploaded_by": e.get("uploaded_by", ""),
                    "uploaded_at": e.get("uploaded_at", datetime.utcnow().isoformat() + "Z"),
                    "tags": e.get("metadata", e.get("tags", {})),
                }
            return out
        if isinstance(raw, dict):
            return raw
        return {}
    except json.JSONDecodeError:
        return {}
    except FileNotFoundError:
        return {}
    except OSError:
        return {}


def _save_index(idx: dict[str, Any]) -> None:
    FILE_INDEX_PATH.write_text(json.dumps(idx, indent=2), encoding="utf-8")


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


def list_file_entries() -> list[dict]:
    """Test-friendly listing that returns entries with `file_id` and `uri` keys.

    This is provided to match older test expectations while preserving
    the canonical `list_files()` API used elsewhere.
    """
    out = []
    for e in list_files():
        out.append(
            {
                "file_id": e.get("id"),
                "filename": e.get("filename"),
                "uri": e.get("blob_uri"),
                "content_type": e.get("content_type"),
                "metadata": e.get("tags", {}),
            }
        )
    return out


def register_file_entry(
    file_id: str,
    filename: str,
    uri: str,
    content_type: str,
    metadata: dict | None = None,
) -> dict:
    """Test helper to register a file entry with a pre-defined id."""
    idx = _load_index()
    entry = {
        "id": file_id,
        "blob_uri": uri,
        "container": "",
        "blob_name": filename,
        "size": 0,
        "filename": filename,
        "content_type": content_type,
        "uploaded_by": "",
        "uploaded_at": datetime.utcnow().isoformat() + "Z",
        "tags": metadata or {},
    }
    idx[file_id] = entry
    _save_index(idx)
    return {
        "file_id": file_id,
        "filename": filename,
        "uri": uri,
        "content_type": content_type,
        "metadata": metadata or {},
    }


def get_file_entry(file_id: str) -> dict:
    idx = _load_index()
    if file_id not in idx:
        raise KeyError("not_found")
    entry = idx[file_id]
    # provide a compatibility alias expected by some tests
    entry.setdefault("file_id", entry.get("id"))
    return entry


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
    entry.setdefault("file_id", entry.get("id"))
    return entry


def delete_file_entry(file_id: str) -> None:
    idx = _load_index()
    if file_id in idx:
        del idx[file_id]
        _save_index(idx)


def task_state_path(task_id: str) -> Path:
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    return TASKS_DIR / f"{task_id}.json"


def write_task_state(task_id: str, payload: dict[str, Any]) -> dict:
    """Write task state.

    If `TASK_STATE_PATH` is set to a Path (tests), write a mapping of task_id -> state
    into that single file. Otherwise keep per-task files under TASKS_DIR (legacy).
    Returns the written state dict.
    """
    # test hook: single file containing mapping
    if TASK_STATE_PATH:
        TASK_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            raw = TASK_STATE_PATH.read_text(encoding="utf-8")
            store = json.loads(raw) if raw else {}
        except Exception:
            store = {}
        state = {"task_id": task_id, **payload}
        store[task_id] = state
        TASK_STATE_PATH.write_text(json.dumps(store, indent=2), encoding="utf-8")
        return state

    path = task_state_path(task_id)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return {"task_id": task_id, **payload}


def get_task_state(task_id: str) -> dict:
    """Read task state from TASK_STATE_PATH (if set) or per-task file."""
    if TASK_STATE_PATH:
        if not TASK_STATE_PATH.exists():
            return {"task_id": task_id, "status": "new"}
        try:
            store = json.loads(TASK_STATE_PATH.read_text(encoding="utf-8"))
            return store.get(task_id, {"task_id": task_id, "status": "new"})
        except Exception:
            return {"task_id": task_id, "status": "new"}

    path = task_state_path(task_id)
    if not path.exists():
        return {"task_id": task_id, "status": "new"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"task_id": task_id, "status": "new"}
