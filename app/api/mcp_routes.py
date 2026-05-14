# app/api/mcp_routes.py
# pylint: disable=too-many-return-statements,broad-exception-caught

from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from app.core.agent_context import AgentContext, get_mcp_context
from app.mcp.registry import TOOL_REGISTRY, list_tools


router = APIRouter(prefix="/mcp", tags=["mcp"])


def _jsonrpc_result(request_id: Any, result: Any) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result,
    }


def _jsonrpc_error(
    request_id: Any,
    code: int,
    message: str,
    data: Any | None = None,
) -> dict[str, Any]:
    error: dict[str, Any] = {
        "code": code,
        "message": message,
    }

    if data is not None:
        error["data"] = data

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": error,
    }

@router.post("/tools/call")
async def mcp_tools_call_compat(
    payload: dict[str, Any],
    ctx: AgentContext = Depends(get_mcp_context),
) -> dict[str, Any]:
    tool_name = payload.get("tool_name")
    arguments = payload.get("arguments") or {}

    if not isinstance(tool_name, str) or not tool_name:
        raise HTTPException(
            status_code=400,
            detail="tool_name_required",
        )

    if not isinstance(arguments, dict):
        raise HTTPException(
            status_code=400,
            detail="arguments_must_be_object",
        )

    handler = TOOL_REGISTRY.get(tool_name)

    if handler is None:
        raise HTTPException(
            status_code=400,
            detail={
                "fail_closed": True,
                "reason": "tool_not_registered",
                "tool": tool_name,
            },
        )

    result = await handler(ctx, arguments)

    return {
        "tool_name": tool_name,
        "result": result,
    }

@router.post("")
async def mcp_jsonrpc(
    payload: dict[str, Any],
    ctx: AgentContext = Depends(get_mcp_context),
) -> dict[str, Any]:
    request_id = payload.get("id")

    if payload.get("jsonrpc") != "2.0":
        return _jsonrpc_error(
            request_id=request_id,
            code=-32600,
            message="Invalid Request",
            data="jsonrpc must be '2.0'",
        )

    method = payload.get("method")
    params = payload.get("params") or {}

    if not isinstance(params, dict):
        return _jsonrpc_error(
            request_id=request_id,
            code=-32602,
            message="Invalid params",
            data="params must be an object",
        )

    try:
        if method == "initialize":
            return _jsonrpc_result(
                request_id=request_id,
                result={
                    "protocolVersion": "2025-11-25",
                    "capabilities": {
                        "tools": {
                            "listChanged": False,
                        }
                    },
                    "serverInfo": {
                        "name": "engineering-agent-control-plane",
                        "version": "0.1.0",
                    },
                },
            )

        if method == "tools/list":
            return _jsonrpc_result(
                request_id=request_id,
                result={
                    "tools": list_tools(),
                },
            )

        if method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments") or {}

            if not isinstance(name, str) or not name:
                return _jsonrpc_error(
                    request_id=request_id,
                    code=-32602,
                    message="Invalid params",
                    data="params.name must be a non-empty string",
                )

            if not isinstance(arguments, dict):
                return _jsonrpc_error(
                    request_id=request_id,
                    code=-32602,
                    message="Invalid params",
                    data="params.arguments must be an object",
                )

            handler = TOOL_REGISTRY.get(name)

            if handler is None:
                return _jsonrpc_error(
                    request_id=request_id,
                    code=-32601,
                    message="Tool not found",
                    data=name,
                )

            result = await handler(ctx, arguments)

            return _jsonrpc_result(
                request_id=request_id,
                result={
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, separators=(",", ":")),
                        }
                    ],
                    "isError": False,
                },
            )

        return _jsonrpc_error(
            request_id=request_id,
            code=-32601,
            message="Method not found",
            data=method,
        )

    except PermissionError as exc:
        return _jsonrpc_result(
            request_id=request_id,
            result={
                "content": [
                    {
                        "type": "text",
                        "text": str(exc),
                    }
                ],
                "isError": True,
            },
        )

    except ValidationError as exc:
        return _jsonrpc_result(
            request_id=request_id,
            result={
                "content": [
                    {
                        "type": "text",
                        "text": exc.json(),
                    }
                ],
                "isError": True,
            },
        )

    except Exception as exc:
        return _jsonrpc_error(
            request_id=request_id,
            code=-32603,
            message="Internal error",
            data=str(exc),
        )


@router.get("/tools/list")
async def mcp_tools_list_compat() -> dict[str, Any]:
    return {
        "tools": list_tools(),
    }
