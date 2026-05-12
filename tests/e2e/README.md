Playwright E2E scaffolding

This scaffold uses Playwright's webServer option so Playwright manages app startup and shutdown (recommended for local and CI).

Quickstart (bash / macOS / Linux):

1. cd tests/e2e
2. npm ci
3. npx playwright install --with-deps
4. npx playwright test

Playwright will start the ASGI app using the webServer command in playwright.config.ts. No manual backgrounding is required.

Quickstart (PowerShell):

1. Set-Location tests\e2e
2. npm ci
3. npx playwright install --with-deps
4. npx playwright test

If you prefer manual lifecycle control (not recommended), start the app in background and capture the PID (bash example):

cd tests/e2e
npm ci
npx playwright install --with-deps

cd ../..
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
APP_PID=$!

cd tests/e2e
npx playwright test

kill $APP_PID

PowerShell manual lifecycle (captures process and ensures cleanup):

$proc = Start-Process -NoNewWindow -FilePath python -ArgumentList '-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8000' -PassThru
try {
  Set-Location tests\e2e
  npx playwright test
} finally {
  Stop-Process -Id $proc.Id -Force
}

Note: For CI reproducibility, commit tests/e2e/package-lock.json and use npm ci in pipelines.
