# CDYP7 Memory Hooks MCP Web App Integration

This bundle adds operational memory hooks, schemas, negative tests, and a curation job spec to the CDYP7 harness.

## Install

Copy into the FastAPI web app repo root:

```text
config/runtime-adapter.memory-extension.yaml
schemas/agent-memory/*.schema.json
app/memory/*.py
app/mcp/memory_tools.py
scripts/validate_memory_layer.py
tests/memory/*
ci/*
docs/MEMORY_HOOKS.md
```

## Validate

```bash
pip install jsonschema PyYAML
python scripts/validate_memory_layer.py
python tests/memory/test_memory_guardrails.py
```

## Boundary

Memory is not evidence. Memory is not authority. Runtime writes are forbidden. Hooks are signals only.
