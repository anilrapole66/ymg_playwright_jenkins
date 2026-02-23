// @ts-check
import { defineConfig, devices } from '@playwright/test';

/**
 * IMPORTANT:
 * Jenkins cannot access "python" command
 * So we use full executable path
 */
const PYTHON = `"C:\\Users\\RAPOLE ANIL KUMAR\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"`;

/**
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './tests',

  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  reporter: 'html',

  use: {
    baseURL: 'http://127.0.0.1:8000/',
    headless: true,
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  /**
   * Start Django automatically before tests
   * Uses SQLite CI DB (settings_ci.py)
   */
  webServer: {
  command: `cd .. && set DJANGO_SETTINGS_MODULE=ymgportal.settings_ci && ${PYTHON} ymgportal/manage.py migrate && ${PYTHON} ymgportal/manage.py runserver 127.0.0.1:8000`,
  url: 'http://127.0.0.1:8000',
  timeout: 120000,
  reuseExistingServer: false
},
});