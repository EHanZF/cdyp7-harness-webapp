# app/mcp/registry.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Awaitable, Callable

from app.mcp.memory_tools import MemorySemanticSearchTool
from app.memory.semantic_search import SemanticSearchService
from app.memory.vector_store import embedder, qdrant_client


ToolHandler = Callable[[Any, dict[str, Any]], Awaitable[dict[str, Any]]]

TOOLS_PATH = Path(__file__).resolve().parent / "tools.json"


def list_tools() -> list[dict[str, Any]]:
    raw = json.loads(TOOLS_PATH.read_text(encoding="utf-8"))

    if isinstance(raw, dict):
        tools = raw.get("tools", [])
    elif isinstance(raw, list):
        tools = raw
    else:
        tools = []

    normalized: list[dict[str, Any]] = []

    for tool in tools:
        if not isinstance(tool, dict):
            continue

        name = tool.get("name")
        if not isinstance(name, str) or not name:
            continue

        normalized.append(
            {
                "name": name,
                "description": tool.get("description", ""),
                "inputSchema": tool.get(
                    "inputSchema",
                    tool.get("input_schema", {}),
                ),
            }
        )

    return normalized


def missing_tool_handler(tool_name: str) -> ToolHandler:
    async def _handler(ctx: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        del ctx
        return {
            "isError": True,
            "error": "tool_not_implemented",
            "tool": tool_name,
            "arguments": arguments,
        }

    return _handler


def build_tool_registry() -> dict[str, Any]:
    semantic_search_tool = MemorySemanticSearchTool(
        SemanticSearchService(
            qdrant=qdrant_client,
            embedder=embedder,
        )
    )

    return {
        "cdyp7.memory.semantic_search": semantic_search_tool,
        "harness.generate_release_sheet": missing_tool_handler(
            "harness.generate_release_sheet"
        ),
        "harness.validate_release_sheet": missing_tool_handler(
            "harness.validate_release_sheet"
        ),
        "harness.write_receipt": missing_tool_handler(
            "harness.write_receipt"
        ),
        "harness.fetch_artifact": missing_tool_handler(
            "harness.fetch_artifact"
        ),
        "harness.resolve_replay": missing_tool_handler(
            "harness.resolve_replay"
        ),
    }


TOOL_REGISTRY = build_tool_registry()
