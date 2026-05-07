from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

HOOKS = {
    "repeat_lifecycle_conflict": "engineering-review",
    "confidence_drift_detected": "stl-attention",
    "repeated_insufficient_evidence": "data-gap-review",
}

def hook_event(hook_id: str, domain: str, payload: dict[str, Any]) -> dict[str, Any]:
    if hook_id not in HOOKS:
        raise ValueError(f"Unknown memory hook: {hook_id}")
    return {
        "event_type": "memory_hook_triggered",
        "hook_id": hook_id,
        "domain": domain,
        "webhook_name": HOOKS[hook_id],
        "payload": payload,
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

def evaluate_stale_semantic_pattern(pattern: dict[str, Any]) -> dict[str, Any]:
    # Deterministic placeholder: production job should compare last_confirmed_utc against current date.
    if pattern.get("last_confirmed") == "90_days_ago":
        return {
            "result": "pattern_invalidated",
            "effects": {"pattern_deprecated": True, "webhook_emitted": "memory-curation-alert"},
        }
    return {"result": "pattern_retained", "effects": {"pattern_deprecated": False}}
