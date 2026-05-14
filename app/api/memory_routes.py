from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.agent_context import AgentContext, get_system_context
from app.memory.semantic_search import SemanticSearchService
from app.memory.vector_store import embedder, qdrant_client
from app.schemas.memory import SemanticSearchRequest, SemanticSearchResponse


router = APIRouter(prefix="/memory", tags=["memory"])


def get_semantic_search_service() -> SemanticSearchService:
    from app.dependencies import embedder, qdrant_client

    return SemanticSearchService(qdrant=qdrant_client, embedder=embedder)


@router.post(
    "/semantic-search",
    response_model=SemanticSearchResponse,
    operation_id="semanticSearch",
)
async def semantic_search_http(
    req: SemanticSearchRequest,
    ctx: AgentContext = Depends(get_system_context),
    svc: SemanticSearchService = Depends(get_semantic_search_service),
) -> SemanticSearchResponse:
    return await svc.search(ctx, req)
