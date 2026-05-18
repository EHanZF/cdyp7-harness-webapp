# app/routes/mcp_validation.py
from fastapi import APIRouter, UploadFile, Form
from app.mcp.validators import (
    validate_features,
    validate_trace,
    validate_graph,
)

router = APIRouter(prefix="/api/mcp")

@router.post("/validate-import")
async def validate_import(
    dataset: str = Form(...),
    file: UploadFile = Form(...)
):
    if dataset == "MCP_FEATURES":
        return validate_features(file)
    if dataset == "FEATURE_REQUIREMENT_TRACE":
        return validate_trace(file)
    if dataset == "FEATURE_REQUIREMENT_VERIFICATION_GRAPH":
        return validate_graph(file)

    return {"valid": False, "error": "Unknown dataset"}
