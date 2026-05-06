#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pip install -e .

python -m pylint --version
python -m pytest --version

<<<<<<< HEAD
echo "Dev environment ready."
=======
echo "Dev environment ready."
>>>>>>> b0f8b70 (Add tooling API contract tests and validation output)
