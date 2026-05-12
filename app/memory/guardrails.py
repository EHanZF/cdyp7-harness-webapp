from __future__ import annotations
from dataclasses import dataclass
from typing import Any

FORBIDDEN_RUNTIME_MEMORY_WRITE = "FORBIDDEN_RUNTIME_MEMORY_WRITE"
MEMORY_DOMAIN_VIOLATION = "MEMORY_DOMAIN_VIOLATION"
MEMORY_AS_AUTHORITY_FORBIDDEN = "MEMORY_AS_AUTHORITY_FORBIDDEN"

@dataclass
class MemoryDecision:
    result: str
    failure_reason: str | None = None
    effects: dict[str, Any] | None = None

def deny(reason: str, **effects: Any) -> MemoryDecision:
    return MemoryDecision(result="denied", failure_reason=reason, effects=effects or {})

def assert_no_runtime_memory_write(actor: str, action: str) -> MemoryDecision | None:
    if action in {"write_semantic_memory", "write_procedural_memory", "mutate_semantic_memory"}:
        return deny(
            FORBIDDEN_RUNTIME_MEMORY_WRITE,
            semantic_memory_modified=False,
            episodic_log_written=True,
            webhook_emitted=False,
        )
    return None

def assert_memory_domain_allowed(run_domain: str, memory_domain: str) -> MemoryDecision | None:
    if run_domain != memory_domain:
        return deny(MEMORY_DOMAIN_VIOLATION, reasoning_executed=False, retrieval_executed=True)
    return None

def assert_memory_not_used_as_evidence(source_refs: list[str]) -> MemoryDecision | None:
    if any(ref.startswith("memory://") for ref in source_refs):
        return deny(MEMORY_AS_AUTHORITY_FORBIDDEN, reasoning_executed=False)
    return None
