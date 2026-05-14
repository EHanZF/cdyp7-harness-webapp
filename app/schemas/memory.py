from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


DocumentType = Literal["requirements", "specification", "analysis", "evidence"]
CatLevel = Literal["CAT1", "CAT2", "CAT3", "CAT4", "CAT5"]


class SemanticSearchFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_type: DocumentType | None = None
    system: str | None = None
    cat_level: CatLevel | None = None


class SemanticSearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    namespace: str
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    filters: SemanticSearchFilters | None = None


class SearchChunkMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    document_type: DocumentType | None = None
    system: str | None = None
    cat_level: CatLevel | None = None
    section: str | None = None
    requirement_id: str | None = None


class SemanticSearchResult(BaseModel):
    chunk_id: str
    document_id: str
    source_uri: str
    text: str
    score: float
    metadata: SearchChunkMetadata


class SemanticSearchResponse(BaseModel):
    results: list[SemanticSearchResult]
    trace_id: str

    @classmethod
    def from_qdrant(cls, hits, trace_id: str) -> "SemanticSearchResponse":
        results: list[SemanticSearchResult] = []

        for hit in hits:
            payload = hit.payload or {}

            results.append(
                SemanticSearchResult(
                    chunk_id=payload["chunk_id"],
                    document_id=payload["document_id"],
                    source_uri=payload.get("source_uri", ""),
                    text=payload.get("text", ""),
                    score=float(hit.score),
                    metadata=SearchChunkMetadata(
                        document_type=payload.get("document_type"),
                        system=payload.get("system"),
                        cat_level=payload.get("cat_level"),
                        section=payload.get("section"),
                        requirement_id=payload.get("requirement_id"),
                    ),
                )
            )

        return cls(results=results, trace_id=trace_id)
