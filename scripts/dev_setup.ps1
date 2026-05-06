$ErrorActionPreference = "Stop"

py -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pip install -e .

python -m pylint --version
python -m pytest --version

<<<<<<< HEAD
Write-Host "Dev environment ready."
=======
Write-Host "Dev environment ready."
>>>>>>> b0f8b70 (Add tooling API contract tests and validation output)
