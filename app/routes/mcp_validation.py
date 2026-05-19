import json
from fastapi import APIRouter, UploadFile, Form

from app.mcp.validators import (
    validate_features,
    validate_trace,
    validate_graph,
)

router = APIRouter(prefix="/api/mcp")


@router.post("/import")
async def import_data(
    dataset: str = Form(...),
    file: UploadFile = Form(...)
):
    content = await file.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return {"success": False, "message": "Invalid JSON"}

    # ✅ Example: validate again (safe guard)
    if dataset == "FEATURE_REQUIREMENT_TRACE":
        result = validate_trace(data)

    elif dataset == "FEATURE_REQUIREMENT_VERIFICATION_GRAPH":
        result = validate_graph(data)

    else:
        return {"success": False, "message": "Unknown dataset"}

    if not result["valid"]:
        return {"success": False, "message": "Validation failed"}

    # ✅ PLACE REAL INGESTION HERE
    # Example:
    # save_to_database(data)

    return {"success": True, "message": "Import completed"}


@router.post("/validate-import")
async def validate_import(
    dataset: str = Form(...),
    file: UploadFile = Form(...),
):
    content = await file.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return {"valid": False, "errors": ["Invalid JSON file"]}

    if dataset == "MCP_FEATURES":
        return validate_features(data)

    if dataset == "FEATURE_REQUIREMENT_TRACE":
        return validate_trace(data)

    if dataset == "FEATURE_REQUIREMENT_VERIFICATION_GRAPH":
        return validate_graph(data)

    return {"valid": False, "error": "Unknown dataset"}
