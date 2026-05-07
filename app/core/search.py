import json
import math
from typing import List

from app.core.config import ROOT
from app.core.embeddings import embed_texts

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
    return search_vectors(query_emb, limit=limit)
