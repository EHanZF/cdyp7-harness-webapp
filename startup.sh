#!/usr/bin/env bash
set -euo pipefail
python scripts/validate_static.py
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
