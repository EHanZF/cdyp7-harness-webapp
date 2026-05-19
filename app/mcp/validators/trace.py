from typing import Any, Dict, List


def validate_trace(trace: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a trace payload.

    Expected structure (example):
    {
        "id": str,
        "steps": list,
        "metadata": dict (optional)
    }
    """

    errors: List[str] = []

    if not isinstance(trace, dict):
        return {"valid": False, "errors": ["Trace must be a dictionary"]}

    # Required fields
    if "id" not in trace:
        errors.append("Missing 'id' field")
    elif not isinstance(trace["id"], str):
        errors.append("'id' must be a string")

    if "steps" not in trace:
        errors.append("Missing 'steps' field")
    elif not isinstance(trace["steps"], list):
        errors.append("'steps' must be a list")
    else:
        for i, step in enumerate(trace["steps"]):
            if not isinstance(step, dict):
                errors.append(f"Step {i} must be an object")
            else:
                if "name" not in step:
                    errors.append(f"Step {i} missing 'name'")
                if "status" not in step:
                    errors.append(f"Step {i} missing 'status'")

    # Optional metadata
    if "metadata" in trace and not isinstance(trace["metadata"], dict):
        errors.append("'metadata' must be a dictionary if provided")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
