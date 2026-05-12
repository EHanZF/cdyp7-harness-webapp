# CDYP7 Memory Hooks Integration

This package adds operational memory hooks to the locked CDYP7 runtime adapter without changing runtime authority.

## Authority Model

```text
Episodic memory: append-only run log, written by orchestrator at end of run.
Semantic memory: curated long-term memory, read-only at runtime, mutated only by memory curator job after approval.
Procedural memory: repo-versioned instructions, read-only at runtime.
```

## Hard Guardrails

```yaml
forbid_runtime_writes: true
forbid_agent_direct_writes: true
forbid_memory_as_evidence: true
forbid_memory_as_authority: true
```

## Hooks

Hooks emit webhooks only after curation. Hooks do not trigger reasoning changes, source mutations, release decisions, or repository updates.

```text
repeat_lifecycle_conflict → engineering-review
confidence_drift_detected → stl-attention
repeated_insufficient_evidence → data-gap-review
```

## Curation Job

The `agent-memory-curator` job runs nightly at `0 2 * * *`. It consolidates episodic entries into curated semantic patterns, deduplicates patterns, decays stale entries, garbage-collects expired episodes, and evaluates hooks.
