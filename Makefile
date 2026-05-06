.PHONY: venv install install-dev validate test smoke run

venv:
	python -m venv .venv

install:
	python -m pip install -r requirements.txt

install-dev:
	python -m pip install -r requirements.txt -r requirements-dev.txt

validate:
	python scripts/validate_static.py

test:
	pytest -q tests/contract

smoke:
	python scripts/smoke_tooling.py

run:
	uvicorn app.main:app --host 127.0.0.1 --port 8000
