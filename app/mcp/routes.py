import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.mcp.validation import validate_tool_input
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

# ✅ Path to tools.json (safe for local + CI)
TOOLS_PATH = Path(__file__).parent / "tools.json"


def load_tools():
    with open(TOOLS_PATH) as f:
        return json.load(f)


# ✅ Tool discovery
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


# ✅ Tool execution
@router.post("/call")
def call_tool(env: ToolEnvelope):
    try:
        # ✅ Enforce actor (important for audit + safety)
        if not env.actor:
            raise ValueError("Actor must be explicit, such as user@example.com")

        # ✅ Validate dynamically against tools.json
        validate_tool_input(env.tool_name, env.arguments)

        # ✅ Dispatch tool execution
        if env.tool_name == "harness.generate_release_sheet":
            result = tooling.generate_release_sheet(
                GenerateReleaseSheetToolRequest(**env.arguments),
                env.actor,
                env.run_id,
            )

        elif env.tool_name == "harness.validate_release_sheet":
            result = tooling.validate_release_sheet(
                ValidateReleaseSheetToolRequest(**env.arguments)
            )

        elif env.tool_name == "harness.write_receipt":
            result = tooling.write_receipt(
                WriteReceiptToolRequest(**env.arguments),
                env.actor,
            )

        elif env.tool_name == "harness.fetch_artifact":
            result = tooling.fetch_artifact(
                FetchArtifactToolRequest(**env.arguments)
            )

        elif env.tool_name == "harness.resolve_replay":
            result = tooling.resolve_replay(
                ResolveReplayToolRequest(**env.arguments)
            )

        else:
            raise ValueError(f"Unknown tool: {env.tool_name}")

        # ✅ Structured result (LLM-friendly)
        return {
            "tool_name": env.tool_name,
            "status": "success",
            "run_id": env.run_id,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "tool_call_failed",
                "message": str(exc),
                "fail_closed": True,
            },
        ) from exc
