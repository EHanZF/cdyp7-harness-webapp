# Copilot instructions for this repository

Purpose: give future Copilot sessions concise, actionable knowledge to work productively.

-- Build, test, and lint (how to run locally)

- Create & activate virtualenv
  - Windows (PowerShell): python -m venv .venv && .\\.venv\\Scripts\\Activate.ps1
  - macOS/Linux (bash): python -m venv .venv && source .venv/bin/activate

- Install dependencies
  - runtime: python -m pip install -r requirements.txt
  - dev: python -m pip install -r requirements.txt -r requirements-dev.txt
  - Makefile aliases: make venv, make install, make install-dev

- Run the app (development)
  - uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
  - make run

- Static validation / CI guards
  - python scripts/validate_static.py
  - make validate (invokes repository guards and static checks)
  - CI hooks live in .github/hooks/ and can be run directly with python

- Tests (pytest)
  - Full suite: pytest
  - Contract tests (Makefile): make test OR pytest -q tests/contract
  - Single file: pytest tests/core/test_authz.py
  - Single test: pytest tests/core/test_authz.py::test_name
  - Match tests: pytest -k <expr>

- E2E Playwright (optional)
  - Location: tests/e2e (scaffolding provided)
  - Playwright uses webServer to manage app lifecycle (recommended). See tests/e2e/playwright.config.ts for configuration.
  - Quickstart (bash):
    - cd tests/e2e
    - npm ci
    - npx playwright install --with-deps
    - npx playwright test
  - Quickstart (PowerShell):
    - Set-Location tests\e2e
    - npm ci
    - npx playwright install --with-deps
    - npx playwright test
  - For CI reproducibility: commit tests/e2e/package-lock.json and use npm ci in pipelines

- Linting & static checks
  - flake8 quick checks used in CI:
    - flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    - flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
  - pylint: pylint app

-- High-level architecture (big picture)

- FastAPI web app
  - Entry: app/main.py
  - Adapter loaded by app.core.config.load_adapter() and stored at app.state.adapter
  - Routers: app/api/* expose the HTTP surface; tooling endpoints under /mcp/tools and /tools/*
  - Static assets served from app/static

- Tooling and contracts
  - Implements a strict CDYP7 tooling surface; tools described in mcp/tools.json
  - scripts/validate_static.py enforces adapter and example consistency (sha256 checks)
  - Contract tests under tests/contract validate the tooling API boundary

- CI and packaging
  - GitHub Actions: .github/workflows/* run validate, lint, and pytest
  - Azure Pipelines: azure-pipelines.yml defines DevSmoke and Deploy stages; startup.sh used by packaging
  - Note: pyproject references src/ layout while runtime code lives in app/; CI may do editable installs or fallback to PYTHONPATH
  - ASGI target used for Playwright and local runs: app.main:app (verify before changing to src-based module paths)

-- Key conventions and repository-specific patterns

- make test runs contract tests only — run pytest for full unit coverage
- pytest addopts include --import-mode=importlib; run tests from repo root for correct discovery
- .env and .env.example guide local env; do not set ENV=production without required AZURE_* vars
- .github/hooks/* enforce static namespace, forbidden refs, policy overrides, schema snapshots, tool allowlists
- examples/ contains tool-call JSON used by validation; update sha256 in scripts/validate_static.py when changing templates

-- External AI assistant configs discovered

- Existing Copilot instructions: .github/copilot-instructions.md (this file)
- MCP tooling descriptor: mcp/tools.json (contains harness.* tool definitions used by runtime and tests)

-- Useful file pointers

- app/main.py
- app/api/
- scripts/validate_static.py
- scripts/smoke_tooling.py
- .github/hooks/
- Makefile
- README.md

(Updated: Playwright uses webServer for lifecycle; ensure package-lock.json is committed for CI reproducibility)
