import os
import importlib
from typing import List


def _ensure_openai_available() -> None:
    try:
        importlib.import_module("openai")
    except Exception as exc:  # pragma: no cover - runtime env dependent
        raise RuntimeError("openai package is required for embeddings; add 'openai' to requirements.txt") from exc


def embed_texts_openai(texts: List[str]) -> List[List[float]]:
    """Use OpenAI embeddings API. Requires OPENAI_API_KEY in the environment."""
    _ensure_openai_available()
    openai = importlib.import_module("openai")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not configured in environment")
    openai.api_key = api_key

    # model choice: text-embedding-3-small is a general purpose embedding model
    resp = openai.Embedding.create(model="text-embedding-3-small", input=texts)
    embeddings: List[List[float]] = [d["embedding"] for d in resp["data"]]
    return embeddings


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Dispatch to available embedding provider. Currently only OpenAI is supported."""
    # Future: detect sentence-transformers or local backends
    return embed_texts_openai(texts)
