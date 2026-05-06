# CDYP7 Harness Tooling API

This bundle updates the FastAPI web app to expose a strict internal tooling API for the Orchestrator.

## Tools

```text
harness.generate_release_sheet
harness.validate_release_sheet
harness.write_receipt
harness.fetch_artifact
harness.resolve_replay
```

## Boundary

The API allows artifact generation, artifact storage, receipt emission, schema validation, and deterministic replay resolution only.

It explicitly does not allow release approval, repository mutation, HITL resolution, policy decision, or requirement authoring.

## MCP endpoints

```text
GET  /mcp/tools/list
POST /mcp/tools/call
```

## REST endpoints

```text
POST /tools/generate-release-sheet
POST /tools/validate-release-sheet
POST /tools/write-receipt
POST /tools/fetch-artifact
POST /tools/resolve-replay
```
