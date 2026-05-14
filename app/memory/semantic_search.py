from __future__ import annotations

from app.core.agent_context import AgentContext
from app.schemas.memory import SemanticSearchRequest, SemanticSearchResponse


class SemanticSearchService:
    def __init__(self, qdrant, embedder):
        self.qdrant = qdrant
        self.embedder = embedder

    async def search(
        self,
        ctx: AgentContext,
        req: SemanticSearchRequest,
    ) -> SemanticSearchResponse:
        ctx.assert_tool_allowed("memory.semantic_search")
        ctx.assert_namespace(req.namespace)

        if req.filters:
            if req.filters.system:
                ctx.assert_system(req.filters.system)

            if req.filters.cat_level:
                ctx.assert_cat_level(req.filters.cat_level)

            if req.filters.document_type:
                ctx.assert_document_type_allowed(req.filters.document_type)

        query_vec = await self.embedder.embed(req.query)

        qdrant_filter = self._build_filter(ctx, req)

        hits = await self.qdrant.search(
            vector=query_vec,
            limit=req.top_k,
            filter=qdrant_filter,
        )

        return SemanticSearchResponse.from_qdrant(
            hits,
            trace_id=ctx.provenance_root,
        )

    def _build_filter(self, ctx: AgentContext, req: SemanticSearchRequest) -> dict:
        must = [
            {"key": "namespace", "match": {"value": ctx.namespace}},
            {"key": "project_id", "match": {"value": ctx.project_id}},
            {"key": "system", "match": {"value": ctx.system}},
            {"key": "cat_level", "match": {"value": ctx.cat_level}},
        ]

        if req.filters and req.filters.document_type:
            must.append(
                {
                    "key": "document_type",
                    "match": {"value": req.filters.document_type},
                }
            )

        return {"must": must}
