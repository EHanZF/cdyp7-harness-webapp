from typing import Any

from fastapi import APIRouter, Body, Header, HTTPException, Request

router = APIRouter()

INTERNAL_RUNTIME_VALUE = "intent-boundary"


def jsonrpc_result(request_id: Any, result: Any) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result,
    }


def jsonrpc_error(
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


@router.post("/mcp")
async def mcp_endpoint(
    request: Request,
    x_internal_runtime: str | None = Header(default=None),
):
    if x_internal_runtime != INTERNAL_RUNTIME_VALUE:
        raise HTTPException(
            status_code=403,
            detail="mcp_endpoint_internal_only",
        )

    payload: Any = await request.json()

    if isinstance(payload, list):
        return jsonrpc_error(
            request_id=None,
            code=-32600,
            message="JSON-RPC batch requests are denied",
        )

    if not isinstance(payload, dict):
        return jsonrpc_error(
            request_id=None,
            code=-32600,
            message="JSON-RPC request must be an object",
        )

    request_id = payload.get("id")

    if payload.get("jsonrpc") != "2.0":
        return jsonrpc_error(
            request_id=request_id,
            code=-32600,
            message="jsonrpc must be 2.0",
        )

    method = payload.get("method")

    if method == "tools/list":
        return jsonrpc_result(
            request_id=request_id,
            result={
                "tools": [
                    {
                        "name": "generate_requirements",
                        "description": "Generate non-authoritative requirement snapshot artifact.",
                        "inputSchema": {
                            "type": "object",
                            "required": [
                                "task_id",
                                "artifact_type",
                                "source",
                                "snapshot",
                                "validation_required",
                                "evidence_scope",
                            ],
                            "properties": {
                                "task_id": {"type": "string"},
                                "artifact_type": {"const": "requirement_snapshot"},
                                "source": {
                                    "type": "string",
                                    "enum": ["ptc", "doors"],
                                },
                                "snapshot": {
                                    "type": "object",
                                    "required": ["$ref"],
                                    "properties": {
                                        "$ref": {"type": "string"},
                                    },
                                },
                                "validation_required": {"type": "boolean"},
                                "evidence_scope": {
                                    "type": "string",
                                    "enum": ["summary", "full"],
                                },
                            },
                            "additionalProperties": False,
                        },
                    },
                    {
                        "name": "releaseSheetReviewTool",
                        "description": "Deterministic release sheet review against exported requirement snapshots.",
                        "inputSchema": {
                            "type": "object",
                            "additionalProperties": True,
                        },
                    },
                    {
                        "name": "math.mapNodeLinks",
                        "description": "Deterministic cosine-similarity node link mapper.",
                        "inputSchema": {
                            "type": "object",
                            "additionalProperties": True,
                        },
                    },
                ]
            },
        )

    if method == "tools/call":
        params = payload.get("params")

        if not isinstance(params, dict):
            return jsonrpc_error(
                request_id=request_id,
                code=-32602,
                message="params must be an object",
            )

        name = params.get("name")
        arguments = params.get("arguments")

        if not isinstance(name, str) or not name:
            return jsonrpc_error(
                request_id=request_id,
                code=-32602,
                message="params.name must be a non-empty string",
            )

        if not isinstance(arguments, dict):
            return jsonrpc_error(
                request_id=request_id,
                code=-32602,
                message="params.arguments must be an object",
            )

        if name == "generate_requirements":
            return jsonrpc_result(
                request_id=request_id,
                result={
                    "content": [
                        {
                            "type": "json",
                            "json": {
                                "status": "accepted",
                                "artifact_type": arguments.get("artifact_type"),
                                "task_id": arguments.get("task_id"),
                                "source": arguments.get("source"),
                                "snapshot": arguments.get("snapshot"),
                                "validation_required": arguments.get("validation_required"),
                                "evidence_scope": arguments.get("evidence_scope"),
                                "authority_effect": "none",
                                "persistence_effect": "none",
                                "promotion_gate": "closed_for_authority",
                            },
                        }
                    ],
                    "isError": False,
                },
            )

        if name == "releaseSheetReviewTool":
            content_field_names = arguments.get("content_field_names", [])

            return jsonrpc_result(
                request_id=request_id,
                result={
                    "content": [
                        {
                            "type": "json",
                            "json": {
                                "status": "accepted",
                                "sheet_id": arguments.get("sheet_id"),
                                "source": arguments.get("source"),
                                "fields_reviewed": len(content_field_names),
                                "authority_effect": "none",
                                "persistence_effect": "none",
                                "promotion_gate": "closed_for_authority",
                            },
                        }
                    ],
                    "isError": False,
                },
            )

        if name == "math.mapNodeLinks":
            nodes = arguments.get("nodes", [])
            policy = arguments.get("policy", {})

            return jsonrpc_result(
                request_id=request_id,
                result={
                    "content": [
                        {
                            "type": "json",
                            "json": {
                                "status": "accepted",
                                "nodeSetId": arguments.get("nodeSetId"),
                                "nodeCount": len(nodes),
                                "metric": policy.get("metric", "cosine"),
                                "authority_effect": "none",
                                "persistence_effect": "none",
                                "promotion_gate": "closed_for_authority",
                            },
                        }
                    ],
                    "isError": False,
                },
            )

        return jsonrpc_error(
            request_id=request_id,
            code=-32000,
            message="Tool execution failed",
            data={
                "reason": "tool_not_registered",
                "tool": name,
            },
        )

    return jsonrpc_error(
        request_id=request_id,
        code=-32601,
        message="Unknown JSON-RPC method",
        data={
            "reason": "unknown_method",
        },
    )
