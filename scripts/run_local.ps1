$env:PYTHONPATH="."
if (Test-Path ".env") {
  Write-Host "Using .env"
}
uvicorn app.main:app --host 127.0.0.1 --port 8000
