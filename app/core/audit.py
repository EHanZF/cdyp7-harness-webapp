import json
from datetime import datetime
from typing import Any

from app.core.config import ROOT

AUDIT_LOG_PATH = ROOT / "artifacts" / "audit.log"
# backwards compat alias
AUDIT_PATH = AUDIT_LOG_PATH


def _ensure_audit_dir():
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not AUDIT_LOG_PATH.exists():
        AUDIT_LOG_PATH.write_text("", encoding="utf-8")


def log_event(event_type: str, correlation_id: str | None, actor: str, details: dict[str, Any]) -> None:
    _ensure_audit_dir()
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "correlation_id": correlation_id,
        "actor": actor,
        "details": details,
    }
    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry))
        fh.write("\n")


def read_audit_lines(limit: int = 200) -> list[dict[str, Any]]:
    _ensure_audit_dir()
    lines = AUDIT_LOG_PATH.read_text(encoding="utf-8").splitlines()
    out: list[dict[str, Any]] = []
    for ln in lines[-limit:]:
        try:
            out.append(json.loads(ln))
        except Exception:
            continue
    return out


def append_audit_event(event_type: str, actor: str, metadata: dict | None = None) -> dict:
    """Append an audit event and return the event dict (test-friendly wrapper)."""
    corr = None
    details = metadata or {}
    _ensure_audit_dir()
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "correlation_id": corr,
        "actor": actor,
        "metadata": details,
    }
    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry))
        fh.write("\n")
    return entry


def list_audit_events(limit: int = 200) -> list[dict]:
    """Test-friendly wrapper around read_audit_lines."""
    return read_audit_lines(limit)
