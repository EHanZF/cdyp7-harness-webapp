from typing import Any

# Placeholder ALM integration layer. Real endpoints should be wired later.


def list_alm_artifacts(system: str, artifact_type: str) -> list[dict[str, Any]]:
    # Return empty placeholder list; real integration will query PTC/Codebeamer
    return []


def perform_alm_action(
    system: str, artifact: str, action: str | None, arguments: dict[str, Any], actor: str, correlation_id: str
) -> dict[str, Any]:
    # Actions that require approval
    approval_required = {"create", "update", "attach", "attach_file"}
    if action in approval_required:
        return {"status": "approval_required", "reason": "action_requires_human_approval"}
    # For read-only or safe actions, return a simple success placeholder
    return {"status": "ok", "action": action, "artifact": artifact}
