import json
from pathlib import Path

from app.mcp.validation import validate_tool_input
from fastapi import APIRouter, HTTPException
from app.core import tooling
from app.core.models import (
    FetchArtifactToolRequest,
    GenerateReleaseSheetToolRequest,
    ResolveReplayToolRequest,
    ToolEnvelope,
    ValidateReleaseSheetToolRequest,
    WriteReceiptToolRequest,
)

# ✅ Router scoped to MCP tools
router = APIRouter(prefix="/mcp/tools", tags=["mcp"])

# ✅ Path to tools.json
TOOLS_PATH = Path("app/mcp/tools.json")


def load_tools():
    with open(TOOLS_PATH) as f:
        return json.load(f)


# ✅ Tool discovery (LLM reads this)
@router.get("/list")
def list_tools():
    data = load_tools()

    tools = []
    for t in data["tools"]:
        tools.append({
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["input_schema"],
            },
        })

    return {"tools": tools}


@router.post("/call")
def call_tool(env: ToolEnvelope):
    try:
        # ✅ Validate dynamically against tools.json
        validate_tool_input(env.tool_name, env.arguments)

        # ✅ Then execute

        if env.tool_name == "harness.generate_release_sheet":
            return {
                "content": tooling.generate_release_sheet(
                    GenerateReleaseSheetToolRequest(**env.arguments),
                    env.actor or "",
                    env.run_id,
                )
            }

        if env.tool_name == "harness.validate_release_sheet":
            return {
                "content": tooling.validate_release_sheet(
                    ValidateReleaseSheetToolRequest(**env.arguments)
                )
            }

        if env.tool_name == "harness.write_receipt":
            return {
                "content": tooling.write_receipt(
                    WriteReceiptToolRequest(**env.arguments),
                    env.actor or "",
                )
            }

        if env.tool_name == "harness.fetch_artifact":
            return {
                "content": tooling.fetch_artifact(
                    FetchArtifactToolRequest(**env.arguments)
                )
            }

        if env.tool_name == "harness.resolve_replay":
            return {
                "content": tooling.resolve_replay(
                    ResolveReplayToolRequest(**env.arguments)
                )
            }

        raise ValueError("unknown_tool")

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "tool_call_failed",
                "message": str(exc),
                "fail_closed": True,
            },
        ) from exc
