// @ts-check
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['junit', { outputFile: 'test-results/junit-report.xml' }],
    ['list'],
  ],

  use: {
    baseURL: 'http://127.0.0.1:8000/',
    headless: true,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  webServer: {
    command: 'set DJANGO_SETTINGS_MODULE=employee_portal.settings_ci && ..\\venv\\Scripts\\python ..\\ymgportal\\manage.py runserver 127.0.0.1:8000 --noreload --nothreading',
    url: 'http://127.0.0.1:8000',
    timeout: 120000,
    reuseExistingServer: !process.env.CI,
  },
});