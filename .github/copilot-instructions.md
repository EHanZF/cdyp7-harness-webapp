# Copilot instructions for this repository

Purpose: give future Copilot sessions the minimal, actionable repository knowledge required to work productively.

-- Build, test, and lint (how to run locally)

- Create a venv (Windows PowerShell):
  - python -m venv .venv
  - .\.venv\Scripts\Activate.ps1
- Install runtime deps: python -m pip install -r requirements.txt
- Install dev deps: python -m pip install -r requirements.txt -r requirements-dev.txt

Make targets (shortcuts):
- make venv            # create virtualenv
- make install         # pip install -r requirements.txt
- make install-dev     # install runtime + dev deps
- make validate        # runs python scripts/validate_static.py (repository guards / static checks)
- make test            # runs contract tests: pytest -q tests/contract
- make smoke           # runs scripts/smoke_tooling.py
- make run             # uvicorn app.main:app --host 127.0.0.1 --port 8000

Pytest / single-test examples
- Run full test suite: pytest
- Run repository contract tests (Makefile): make test OR pytest -q tests/contract
- Run a single test file: pytest tests/core/test_authz.py
- Run a single test function: pytest tests/core/test_authz.py::test_name
- Use -k <expr> for expression matching and -q to quiet output

Linting & static checks
- CI uses flake8 as primary lint guard. Locally run:
  - flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
  - flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
- Pylint is configured in pyproject.toml. Run: pylint app  (or pylint src if packaging is used)
- Repository guards executed in CI are in .github/hooks/*.py; they should be run for PR pre-checks.

-- High-level architecture (big picture)

- FastAPI web app entrypoint: app/main.py
  - Loads an "adapter" via app.core.config.load_adapter() and stores it at app.state.adapter
  - Mounts routers from app.api.*: core HTTP surface lives under those routers
  - Static assets served from app/static; index served at GET /
- Tooling API: endpoints expose the MCP tooling surface and specialized tooling endpoints under /mcp/tools and /tools/* (see README tooling surface list)
- Runtime helpers & scripts:
  - scripts/validate_static.py  — static/contract validation used by CI and make validate
  - scripts/smoke_tooling.py    — a smoke runner used by make smoke and pipelines
- CI and pipelines:
  - GitHub Actions workflow at .github/workflows/python-app.yml installs deps, runs repository guards, lints (flake8), and runs pytest
  - Azure Pipelines (azure-pipelines.yml) includes DevSmoke, Build_Test and Deploy stages; packaging step zips repository and uses startup.sh to launch on Azure Web App

-- Key repository conventions and gotchas

- Tests: pytest.ini / pyproject define testpaths=tests and addopts include --import-mode=importlib. Prefer running pytest from repository root.
- Makefile test target intentionally targets contract tests (tests/contract). Do not assume make test runs the full unit test suite.
- CI repository guards: .github/hooks contain scripts that enforce static namespace, forbidden references, tool allowlists, policy overrides and schema snapshots. Run them locally before opening PRs if you need parity with CI.
- Environment: .env and .env.example are present. In production the app enforces AZURE storage config (see app/main.py) — ensure ENV!=production locally unless those variables are set.
- Packaging: pyproject references a src/ packaging layout but runtime code lives in app/. Some CI jobs attempt editable install (pip install -e ".[dev]") and fall back to setting PYTHONPATH if editable install fails.
- Contract tests and tooling contracts: the repository has specialized contract tests under tests/contract—these validate the MCP tooling API boundary and are critical for runtime compatibility.
- Optional allowlist: CI will run tool_allowlist_guard.py only if contracts/cdyp7-tool-allowlist.yaml exists. If you add or update allowlists, keep the file in contracts/ and CI will validate it.

-- Useful file pointers (entry points for automation)
- app/main.py                — FastAPI entry
- app/api/                   — HTTP routers and handler implementations
- .github/hooks/*            — CI guards and static checks used on PRs
- scripts/validate_static.py — local/CI static validator
- scripts/smoke_tooling.py   — smoke runner used by DevSmoke pipeline
- Makefile                   — common local targets
- README.md                  — quickstart and tooling surface



(Generated: Copilot instructions file)
