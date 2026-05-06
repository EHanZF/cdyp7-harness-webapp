Summary

This PR adds a small, scoped set of developer helpers and a non‑prod CI stage to make local development and non‑production smoke testing easier and more deterministic.

Files added

- `requirements-dev.txt` — dev-only dependencies (uvicorn, httpx, pytest, pytest-cov, python-dotenv)
- `Makefile` — convenience targets: `venv`, `install`, `install-dev`, `validate`, `test`, `smoke`, `run`
- `scripts/run_local.ps1` — Windows helper to set `PYTHONPATH` and run uvicorn
- `scripts/ci_install_dev.ps1` — PowerShell helper for CI to optionally install `requirements-dev.txt`
- `.env.example` — placeholder environment variables for local testing

Files changed

- `scripts/smoke_tooling.py` — robustified: try HTTP against a running server, and if unavailable fall back to direct invocation of `app.core.tooling` (useful when FastAPI/uvicorn or native wheels are not installed)
- `app/core/release_sheet_validator.py` — fix unterminated string literal and replace ternary statements with explicit `if/else` for clarity
- `app/main.py` — add a small startup guard to ensure `AZURE_STORAGE_ACCOUNT_URL` is set when `ENV=production` (fails closed in prod)
- `README.md` — add Local Development section with instructions
- `azure-pipelines.yml` — add a conditional `DevSmoke` stage (runs on `develop`) that installs optional dev deps and runs `validate` + smoke

Rationale

- Improve local developer experience: one-command targets to run tests and smoke checks.
- Provide a safe non‑prod CI signal (`DevSmoke`) that does not affect `main`/release pipelines.
- Make smoke testing robust in environments where building native wheels (e.g., `pydantic-core`) is problematic by providing a direct-invocation fallback.

Testing performed

- `python scripts/validate_static.py` — OK
- `python tests/contract/test_tooling_api_contract.py` — OK
- `python scripts/smoke_tooling.py` — ran the fallback direct invocation path (server not running) and generated the artifact:
  - `artifacts/BRK_GM_E2UL_System_Release_Sheet_S011_CAT5.docx`
  - SHA256 returned by the tool: `sha256:2774f5b34a0294be15fdc84c174662a7cc493db39297d11b91945a88337bd25f`

Notes & recommendations

- Installing the full `requirements.txt` on some machines may attempt to build `pydantic-core` from source, which pulls in a Rust toolchain. If you see failures during `pip install` for `pydantic-core`, either:
  - Use Python 3.12 (recommended) where prebuilt wheels are available, or
  - Ensure a Rust toolchain is available on the build agent / developer machine.

- The direct-invocation smoke fallback is intentional and only used for local/dev convenience. It does not alter production runtime behavior.

Production safety

- The change to `app/main.py` adds a guard that will raise at startup if `ENV=production` and `AZURE_STORAGE_ACCOUNT_URL` is not set. This prevents accidental local-file fallback in production.

How to apply locally

```bash
git checkout -b feat/dev-helpers
git apply dev-helpers.patch
git add -A
git commit -m "chore(dev): add dev helpers, robust smoke script, DevSmoke CI stage; fix validator syntax"
git push origin feat/dev-helpers
```

Open a PR with the title in `PR_TITLE.txt` and the body in `PR_BODY.md`.

<<<<<<< HEAD
If you prefer, I can initialize a temporary git branch in this workspace and commit the changes for you — say “init & push” with the remote URL and I will proceed (requires remote/credentials).
=======
If you prefer, I can initialize a temporary git branch in this workspace and commit the changes for you — say “init & push” with the remote URL and I will proceed (requires remote/credentials).
>>>>>>> b0f8b70 (Add tooling API contract tests and validation output)
