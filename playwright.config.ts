import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: 'tests/e2e',
  timeout: 30000,
  expect: { timeout: 5000 },
  fullyParallel: false,
  retries: process.env.CI ? 2 : 0,

  reporter: [
    ['list'],
    ['junit', { outputFile: 'results/junit.xml' }],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
  ],
  use: {
    baseURL: 'http://127.0.0.1:8000',
    headless: true,
    viewport: { width: 1280, height: 720 },
    actionTimeout: 0,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },

  webServer: {
    command: 'PYTHONPATH=. python -m uvicorn main:app --app-dir app --host 127.0.0.1 --port 8000',
    url: 'http://127.0.0.1:8000/',
    reuseExistingServer: true,
    timeout: 30000,
  },

  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],

});
