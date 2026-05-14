# app/memory/vector_store.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class FakeHit:
    payload: dict[str, Any]
    score: float


class LocalEmbedder:
    async def embed(self, text: str) -> list[float]:
        del text
        return [0.0, 0.0, 0.0]


class LocalQdrantClient:
    def __init__(self) -> None:
        self.last_filter: dict[str, Any] | None = None

    async def search(
        self,
        vector: list[float],
        limit: int,
        filter: dict[str, Any],
    ) -> list[FakeHit]:
        del vector

        self.last_filter = filter

        hits = [
            FakeHit(
                payload={
                    "chunk_id": "cdyp7/req-doc-123/7",
                    "document_id": "req-doc-123",
                    "source_uri": "blob://requirements/req-doc-123.pdf",
                    "text": (
                        "The braking system shall enter degraded mode within "
                        "100ms of sensor failure."
                    ),
                    "document_type": "requirements",
                    "system": "ABS",
                    "cat_level": "CAT3",
                    "section": "4.2.1",
                    "requirement_id": "ABS-FH-042",
                },
                score=0.87,
            )
        ]

        return hits[:limit]


embedder = LocalEmbedder()
qdrant_client = LocalQdrantClient()
