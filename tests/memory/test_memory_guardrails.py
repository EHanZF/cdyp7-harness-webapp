#!/usr/bin/env python3
from app.memory.guardrails import assert_no_runtime_memory_write, assert_memory_domain_allowed, assert_memory_not_used_as_evidence
from app.memory.hooks import evaluate_stale_semantic_pattern

poison = assert_no_runtime_memory_write('CDYP71', 'write_semantic_memory')
assert poison is not None
assert poison.result == 'denied'
assert poison.failure_reason == 'FORBIDDEN_RUNTIME_MEMORY_WRITE'
assert poison.effects['semantic_memory_modified'] is False

cross = assert_memory_domain_allowed('brakes', 'steering')
assert cross is not None
assert cross.result == 'denied'
assert cross.failure_reason == 'MEMORY_DOMAIN_VIOLATION'

mem_evidence = assert_memory_not_used_as_evidence(['memory://semantic/pattern-1'])
assert mem_evidence is not None
assert mem_evidence.failure_reason == 'MEMORY_AS_AUTHORITY_FORBIDDEN'

drift = evaluate_stale_semantic_pattern({'id': 'lifecycle_status_conflict', 'last_confirmed': '90_days_ago'})
assert drift['result'] == 'pattern_invalidated'
assert drift['effects']['pattern_deprecated'] is True
print('OK memory guardrail negative tests')
