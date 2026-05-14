import pytest

from app.mcp.memory_tools import MemorySemanticSearchTool


@pytest.mark.asyncio
async def test_mcp_memory_tool_validates_arguments(ctx, semantic_search_service):
    tool = MemorySemanticSearchTool(semantic_search_service)

    result = await tool(
        ctx,
        {
            "namespace": ctx.namespace,
            "query": "ABS degraded mode",
            "top_k": 5,
        },
    )

    assert "results" in result
    assert "trace_id" in result


@pytest.mark.asyncio
async def test_mcp_memory_tool_rejects_extra_arguments(ctx, semantic_search_service):
    tool = MemorySemanticSearchTool(semantic_search_service)

    with pytest.raises(Exception):
        await tool(
            ctx,
            {
                "namespace": ctx.namespace,
                "query": "ABS degraded mode",
                "top_k": 5,
                "unexpected": "nope",
            },
        )
