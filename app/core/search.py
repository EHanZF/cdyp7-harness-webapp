import json
import math
from datetime import datetime
from typing import List

from app.core.config import ROOT
from app.core.embeddings import embed_texts
from app.core.file_index import get_file_entry

VECSTORE_PATH = ROOT / "artifacts" / "vecstore.json"


def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    if len(a) != len(b):
        # pad shorter with zeros
        min_len = min(len(a), len(b))
        a = a[:min_len]
        b = b[:min_len]
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _load_vecstore() -> List[dict]:
    try:
        if not VECSTORE_PATH.exists():
            return []
        raw = VECSTORE_PATH.read_text(encoding="utf-8")
        data = json.loads(raw)
        return data.get("vectors", [])
    except (json.JSONDecodeError, FileNotFoundError, OSError):
        return []


def search_vectors(query_embedding: List[float], limit: int = 5) -> List[dict]:
    vectors = _load_vecstore()
    scores = []
    for v in vectors:
        emb = v.get("embedding")
        if not emb:
            continue
        score = cosine_similarity(query_embedding, emb)
        scores.append({"id": v.get("id"), "file_id": v.get("file_id"), "text": v.get("text"), "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:limit]


def search(query: str, limit: int = 5) -> List[dict]:
    if not query or not query.strip():
        return []
    emb_list = embed_texts([query])
    if not emb_list:
        return []
    query_emb = emb_list[0]
    results = search_vectors(query_emb, limit=limit)
    # enrich with file metadata from file_index where available
    enriched: List[dict] = []
    for r in results:
        file_id = r.get("file_id")
        try:
            entry = get_file_entry(file_id)
            file_meta = {
                "file_id": file_id,
                "filename": entry.get("filename"),
                "content_type": entry.get("content_type"),
                "uri": entry.get("blob_uri"),
                "uploaded_at": entry.get("uploaded_at"),
                "metadata": entry.get("tags", {}),
            }
        except Exception:
            file_meta = {"file_id": file_id, "missing": True}
        newr = dict(r)
        newr["file"] = file_meta
        enriched.append(newr)
    return enriched


def _parse_iso(ts: str):
    if not ts:
        return None
    try:
        # strip trailing Z if present
        if ts.endswith("Z"):
            ts = ts[:-1]
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def _apply_filters(results: List[dict], filters: dict | None) -> List[dict]:
    if not filters:
        return results
    out = []
    tags = filters.get("tags") or {}
    file_ids = set(filters.get("file_ids") or [])
    min_score = filters.get("min_score")
    uploaded_after = _parse_iso(filters.get("uploaded_after") or "")
    uploaded_before = _parse_iso(filters.get("uploaded_before") or "")
    content_type = filters.get("content_type")

    for r in results:
        # filter by file_ids if provided
        if file_ids and (r.get("file_id") not in file_ids):
            continue

        # filter by score
        if min_score is not None:
            try:
                if float(r.get("score", 0.0)) < float(min_score):
                    continue
            except Exception:
                continue

        f = r.get("file") or {}
        # filter by tags (all must match)
        meta = f.get("metadata") or {}
        matched = True
        for k, v in (tags.items() if isinstance(tags, dict) else []):
            if k not in meta:
                matched = False
                break
            if v is not None and str(meta.get(k)) != str(v):
                matched = False
                break
        if not matched:
            continue

        # content type
        if content_type and f.get("content_type") != content_type:
            continue

        # date filters
        uploaded_at_dt = _parse_iso(f.get("uploaded_at") or "")
        if uploaded_after and (not uploaded_at_dt or uploaded_at_dt < uploaded_after):
            continue
        if uploaded_before and (not uploaded_at_dt or uploaded_at_dt > uploaded_before):
            continue

        out.append(r)
    return out


def search_with_filters(query: str, limit: int = 5, filters: dict | None = None) -> List[dict]:
    """Search and apply advanced filters. Backwards-compatible wrapper around `search`.

    Existing callers can continue using `search(query, limit)`; when filters are
    provided, use this helper to perform filtering.
    """
    results = search(query, limit=limit)
    return _apply_filters(results, filters)
