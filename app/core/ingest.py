import io
import json
import uuid
from datetime import datetime
from typing import List

from app.core.config import ROOT
from app.core.file_index import get_file_entry
from app.core.storage import blob_store
from app.core.audit import log_event
from app.core.embeddings import embed_texts

JOBS_PATH = ROOT / "artifacts" / "ingest_jobs.json"
VECSTORE_PATH = ROOT / "artifacts" / "vecstore.json"


def _ensure_jobs():
    JOBS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not JOBS_PATH.exists():
        JOBS_PATH.write_text(json.dumps({}), encoding="utf-8")


def _load_jobs() -> dict:
    _ensure_jobs()
    try:
        return json.loads(JOBS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError, OSError):
        return {}


def _save_jobs(j: dict) -> None:
    JOBS_PATH.write_text(json.dumps(j, indent=2), encoding="utf-8")


def _extract_text_from_bytes(filename: str, data: bytes) -> str:
    name = filename.lower()
    if name.endswith(".txt") or name.endswith(".md") or name.endswith(".csv"):
        return data.decode("utf-8", errors="replace")
    if name.endswith(".docx"):
        try:
            from docx import Document

            doc = Document(io.BytesIO(data))
            paragraphs = [p.text for p in doc.paragraphs if p.text]
            return "\n\n".join(paragraphs)
        except Exception:
            return ""
    if name.endswith(".pdf"):
        try:
            import importlib

            pypdf = importlib.import_module("pypdf")
            reader = pypdf.PdfReader(io.BytesIO(data))
            pages = [p.extract_text() or "" for p in reader.pages]
            return "\n\n".join(pages)
        except Exception:
            return ""
    # fallback: try to decode
    try:
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def _chunk_text(text: str, max_chars: int = 2000) -> List[str]:
    if not text:
        return []
    chunks: List[str] = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + max_chars, length)
        # try to split at last newline or space
        if end < length:
            split_at = text.rfind("\n", start, end)
            if split_at == -1:
                split_at = text.rfind(" ", start, end)
            if split_at > start:
                end = split_at
        chunks.append(text[start:end].strip())
        start = end
    return [c for c in chunks if c]


def start_ingest_job(file_ids: list[str], initiated_by: str) -> str:
    jobs = _load_jobs()
    job_id = str(uuid.uuid4())
    job = {
        "id": job_id,
        "files": file_ids,
        "status": "running",
        "initiated_by": initiated_by,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "result": None,
    }
    jobs[job_id] = job
    _save_jobs(jobs)

    vectors = []
    try:
        for file_id in file_ids:
            entry = get_file_entry(file_id)
            data = blob_store.read_bytes(entry["container"], entry["blob_name"])
            text = _extract_text_from_bytes(entry.get("filename", ""), data)
            chunks = _chunk_text(text)
            if not chunks:
                continue
            # compute embeddings in batches
            embeddings = embed_texts(chunks)
            for idx, chunk in enumerate(chunks):
                vectors.append(
                    {
                        "id": f"{file_id}:{idx}",
                        "file_id": file_id,
                        "text": chunk,
                        "embedding": embeddings[idx],
                    }
                )

        # persist vectors
        VECSTORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            if VECSTORE_PATH.exists():
                existing = json.loads(VECSTORE_PATH.read_text(encoding="utf-8"))
            else:
                existing = {"vectors": []}
        except (json.JSONDecodeError, FileNotFoundError, OSError):
            existing = {"vectors": []}
        existing["vectors"].extend(vectors)
        VECSTORE_PATH.write_text(json.dumps(existing, indent=2), encoding="utf-8")

        job["status"] = "completed"
        job["completed_at"] = datetime.utcnow().isoformat() + "Z"
        job["result"] = {"indexed": len(vectors)}
        jobs[job_id] = job
        _save_jobs(jobs)
        log_event("ingest.complete", job_id, initiated_by, {"indexed": len(vectors)})
    except Exception as exc:  # pragma: no cover - external services may fail
        job["status"] = "failed"
        job["completed_at"] = datetime.utcnow().isoformat() + "Z"
        job["result"] = {"error": str(exc)}
        jobs[job_id] = job
        _save_jobs(jobs)
        log_event("ingest.failed", job_id, initiated_by, {"error": str(exc)})

    return job_id


def get_ingest_job(job_id: str) -> dict | None:
    jobs = _load_jobs()
    return jobs.get(job_id)
