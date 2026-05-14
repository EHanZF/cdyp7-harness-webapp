# app/core/agent_context.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgentContext:
    namespace: str
    project_id: str
    system: str
    cat_level: str
    allowed_tools: set[str] = field(default_factory=set)
    memory_policy: dict[str, Any] = field(default_factory=dict)
    provenance_root: str = "prov/local-dev"

    def assert_tool_allowed(self, tool_name: str) -> None:
        if tool_name not in self.allowed_tools:
            raise PermissionError(f"Tool not allowed: {tool_name}")

    def assert_namespace(self, namespace: str) -> None:
        if namespace != self.namespace:
            raise PermissionError(
                f"Namespace escape blocked: requested={namespace}, "
                f"allowed={self.namespace}"
            )

    def assert_system(self, system: str) -> None:
        if system != self.system:
            raise PermissionError(
                f"System scope mismatch: requested={system}, "
                f"allowed={self.system}"
            )

    def assert_cat_level(self, cat_level: str) -> None:
        if cat_level != self.cat_level:
            raise PermissionError(
                f"CAT scope mismatch: requested={cat_level}, "
                f"allowed={self.cat_level}"
            )

    def assert_document_type_allowed(self, document_type: str) -> None:
        allowed = self.memory_policy.get("allowed_document_types", [])
        if document_type not in allowed:
            raise PermissionError(f"Document type not allowed: {document_type}")


def get_system_context() -> AgentContext:
    return _default_context()


def get_mcp_context() -> AgentContext:
    return _default_context()


def _default_context() -> AgentContext:
    return AgentContext(
        namespace="cdyp7",
        project_id="brake-platform-2026",
        system="ABS",
        cat_level="CAT3",
        allowed_tools={
            "memory.semantic_search",
            "harness.generate_release_sheet",
            "harness.validate_release_sheet",
            "harness.write_receipt",
            "harness.fetch_artifact",
            "harness.resolve_replay",
        },
        memory_policy={
            "allowed_document_types": [
                "requirements",
                "specification",
                "analysis",
                "evidence",
            ],
            "max_chunks_per_query": 10,
        },
        provenance_root="prov/local-dev",
    )
