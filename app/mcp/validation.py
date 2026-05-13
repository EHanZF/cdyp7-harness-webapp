import json
from pathlib import Path
from jsonschema import validate, ValidationError

TOOLS_PATH = Path("app/mcp/tools.json")

# Load once (performance)
with open(TOOLS_PATH) as f:
    TOOLS = json.load(f)["tools"]

# Build quick lookup
TOOL_SCHEMAS = {tool["name"]: tool["input_schema"] for tool in TOOLS}


def validate_tool_input(tool_name: str, arguments: dict):
    if tool_name not in TOOL_SCHEMAS:
        raise ValueError(f"Unknown tool schema: {tool_name}")

    schema = TOOL_SCHEMAS[tool_name]

    try:
        validate(instance=arguments, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Invalid input for {tool_name}: {e.message}")
