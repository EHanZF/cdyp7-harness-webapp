import pytest

from app.memory.semantic_search import SemanticSearchService
from app.schemas.memory import SemanticSearchRequest, SemanticSearchFilters


@pytest.mark.asyncio
async def test_semantic_search_enforces_namespace(ctx, fake_qdrant, fake_embedder):
    svc = SemanticSearchService(qdrant=fake_qdrant, embedder=fake_embedder)

    req = SemanticSearchRequest(
        namespace="wrong-namespace",
        query="ABS degraded mode",
        top_k=5,
    )

    with pytest.raises(PermissionError, match="Namespace"):
        await svc.search(ctx, req)


@pytest.mark.asyncio
async def test_semantic_search_adds_hard_scope_filter(ctx, fake_qdrant, fake_embedder):
    svc = SemanticSearchService(qdrant=fake_qdrant, embedder=fake_embedder)

    req = SemanticSearchRequest(
        namespace=ctx.namespace,
        query="ABS degraded mode",
        top_k=5,
        filters=SemanticSearchFilters(
            document_type="requirements",
            system=ctx.system,
            cat_level=ctx.cat_level,
        ),
    )

    await svc.search(ctx, req)

    qdrant_filter = fake_qdrant.last_filter

    assert {
        "key": "namespace",
        "match": {"value": ctx.namespace},
    } in qdrant_filter["must"]

    assert {
        "key": "project_id",
        "match": {"value": ctx.project_id},
    } in qdrant_filter["must"]

    assert {
        "key": "system",
        "match": {"value": ctx.system},
    } in qdrant_filter["must"]

    assert {
        "key": "cat_level",
        "match": {"value": ctx.cat_level},
    } in qdrant_filter["must"]
