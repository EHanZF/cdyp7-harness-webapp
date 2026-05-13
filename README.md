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
=======
# CDYP7 Runtime Harness Tooling API — Azure App Service + Blob

This bundle updates the Harness SW for the web app with the strict CDYP7 Tooling API.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/validate_static.py
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Local Development

### Prereqs
- Python 3.12+
- pip

### Setup
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
```

### Validate & Test

```bash
make validate
make test
```

### Run

```bash
make run
```

### Smoke Test

```bash
make smoke
```

### CI helper (PowerShell)
If you want to add a non-production/dev stage in Azure DevOps that installs dev dependencies, the repository includes `scripts/ci_install_dev.ps1`. Example Azure Pipelines snippet:

```yaml
- stage: DevSmoke
  displayName: 'Dev: smoke and validation (non-prod)'
  condition: and(succeeded(), eq(variables['Build.SourceBranchName'], 'develop'))
  jobs:
    - job: InstallDev
      pool:
        vmImage: 'ubuntu-latest'
      steps:
        - powershell: pwsh ./scripts/ci_install_dev.ps1
          displayName: 'Install dev requirements'
        - script: make validate
          displayName: 'Run static validation'
```

## Tooling surface

```text
GET  /mcp/tools/list
POST /mcp/tools/call
POST /tools/generate-release-sheet
POST /tools/validate-release-sheet
POST /tools/write-receipt
POST /tools/fetch-artifact
POST /tools/resolve-replay
```

## Azure DevOps

Use:

```text
azure-pipelines.yml
```

## Template hash

```text
sha256:c82c036d9c3661e108f8c0a52443a9dae2d8d40479dc2a2a419e9960625cef7c
>>>>>>> b0f8b70 (Add tooling API contract tests and validation output)
```

## Boundary

Memory is not evidence. Memory is not authority. Runtime writes are forbidden. Hooks are signals only.

```text
Execution + evidence only.
No release approval.
No repository mutation.
No HITL resolution.
No policy decision.
No requirement authoring.
```
