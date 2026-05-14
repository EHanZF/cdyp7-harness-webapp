# tests/conftest.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.agent_context import AgentContext
from app.main import app
from app.memory.semantic_search import SemanticSearchService


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def ctx() -> AgentContext:
    return AgentContext(
        namespace="cdyp7",
        project_id="brake-platform-2026",
        system="ABS",
        cat_level="CAT3",
        allowed_tools={
            "memory.semantic_search",
            "harness.generate_release_sheet",
            "harness.validate_release_sheet",
            "harness.write_receipt",
            "harness.fetch_artifact",
            "harness.resolve_replay",
        },
        memory_policy={
            "allowed_document_types": [
                "requirements",
                "specification",
                "analysis",
                "evidence",
            ],
            "max_chunks_per_query": 10,
        },
        provenance_root="prov/test-run",
    )


class FakeEmbedder:
    async def embed(self, text: str) -> list[float]:
        del text
        return [0.0, 0.0, 0.0]


@dataclass
class FakeHit:
    payload: dict[str, Any]
    score: float


class FakeQdrant:
    def __init__(self) -> None:
        self.last_filter: dict[str, Any] | None = None

    async def search(
        self,
        vector: list[float],
        limit: int,
        filter: dict[str, Any],
    ) -> list[float]:
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


@pytest.fixture
def fake_embedder() -> FakeEmbedder:
    return FakeEmbedder()


@pytest.fixture
def fake_qdrant() -> FakeQdrant:
    return FakeQdrant()


@pytest.fixture
def semantic_search_service(
    fake_qdrant: FakeQdrant,
    fake_embedder: FakeEmbedder,
) -> SemanticSearchService:
    return SemanticSearchService(
        qdrant=fake_qdrant,
        embedder=fake_embedder,
    )
