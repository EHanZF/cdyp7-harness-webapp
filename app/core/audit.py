import json
from datetime import datetime
from typing import Any

from app.core.config import ROOT

AUDIT_PATH = ROOT / "artifacts" / "audit.log"


def _ensure_audit_dir():
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not AUDIT_PATH.exists():
        AUDIT_PATH.write_text("", encoding="utf-8")


def log_event(event_type: str, correlation_id: str | None, actor: str, details: dict[str, Any]) -> None:
    _ensure_audit_dir()
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "correlation_id": correlation_id,
        "actor": actor,
        "details": details,
    }
    with AUDIT_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry))
        fh.write("\n")


def read_audit_lines(limit: int = 200) -> list[dict[str, Any]]:
    _ensure_audit_dir()
    lines = AUDIT_PATH.read_text(encoding="utf-8").splitlines()
    out: list[dict[str, Any]] = []
    for ln in lines[-limit:]:
        try:
            out.append(json.loads(ln))
        except Exception:
            continue
    return out
