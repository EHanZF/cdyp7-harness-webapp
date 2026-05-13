#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=.

echo "Starting MCP API..."
echo "Validating static configuration..."

python scripts/validate_static.py

echo "Launching FastAPI app..."

uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2
