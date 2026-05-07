#!/usr/bin/env python3
from pathlib import Path
import json, yaml
from jsonschema import Draft202012Validator

root = Path(__file__).resolve().parents[1]
ext = yaml.safe_load((root / 'config/runtime-adapter.memory-extension.yaml').read_text())
assert ext['memory']['enabled'] is True
assert ext['memory']['semantic']['read_only_at_runtime'] is True
assert ext['memory']['semantic']['write_policy']['writer'] == 'memory_curator_job'
assert ext['memory']['semantic']['write_policy']['approval_required'] is True
assert ext['memory_guardrails']['forbid_runtime_writes'] is True
assert ext['memory_guardrails']['forbid_agent_direct_writes'] is True
assert ext['memory_guardrails']['forbid_memory_as_evidence'] is True
assert ext['memory_guardrails']['forbid_memory_as_authority'] is True
assert ext['memory_hooks']['evaluation_mode'] == 'post_curation_only'
for schema_path in (root / 'schemas/agent-memory').glob('*.schema.json'):
    schema = json.loads(schema_path.read_text())
    Draft202012Validator.check_schema(schema)
print('OK memory layer static assertions')
