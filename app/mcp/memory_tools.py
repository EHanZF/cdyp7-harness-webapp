from __future__ import annotations
from typing import Any
from app.memory.guardrails import assert_no_runtime_memory_write, assert_memory_domain_allowed
from app.memory.hooks import evaluate_stale_semantic_pattern
from app.memory.semantic_search import SemanticSearchService
from app.schemas.memory import SemanticSearchRequest


class MemorySemanticSearchTool:
    name = "cdyp7.memory.semantic_search"

    def __init__(self, service: SemanticSearchService):
        self.service = service

    async def __call__(self, ctx, arguments: dict) -> dict:
        req = SemanticSearchRequest.model_validate(arguments)
        res = await self.service.search(ctx, req)
        return res.model_dump()


async def memory_runtime_write_attempt(args: dict[str, Any]) -> dict[str, Any]:
    decision = assert_no_runtime_memory_write(args.get("actor", "CDYP71"), args.get("action", "write_semantic_memory"))
    if decision:
        return decision.__dict__
    return {"result": "allowed"}

async def memory_cross_domain_access(args: dict[str, Any]) -> dict[str, Any]:
    decision = assert_memory_domain_allowed(args.get("domain"), args.get("memory_ref", {}).get("domain"))
    if decision:
        return decision.__dict__
    return {"result": "allowed"}

async def memory_drift_check(args: dict[str, Any]) -> dict[str, Any]:
    return evaluate_stale_semantic_pattern(args.get("semantic_pattern", {}))
