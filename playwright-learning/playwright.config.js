// @ts-check
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  globalSetup: './tests/globalSetup.js',

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
      // All admin tests except logout — logout must run last
      name: 'admin',
      testMatch: /tests[\\/](?!logout\.spec\.js)[^/\\]+\.spec\.js$/,
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/admin.json',
      },
    },
    {
      // Admin logout — runs only after all admin tests complete
      name: 'admin-logout',
      testMatch: /tests[\\/]logout\.spec\.js$/,
      dependencies: ['admin'],
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/admin.json',
      },
    },
    {
      // All employee tests except logout — sequential to avoid session conflicts
      name: 'employee',
      testMatch: /tests[\\/]employee[\\/](?!logout\.spec\.js).+\.spec\.js$/,
      fullyParallel: false,
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/employee.json',
      },
    },
    {
      // Employee logout — runs only after all employee tests complete
      name: 'employee-logout',
      testMatch: /tests[\\/]employee[\\/]logout\.spec\.js$/,
      dependencies: ['employee'],
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/employee.json',
      },
    },
  ],

  // PYTHONPATH and DJANGO_SETTINGS_MODULE are passed from Jenkinsfile via environment
  // so Django can find the employee_portal module correctly
  webServer: {
    // In CI the venv is created by Jenkins at ../venv.
    // Locally, system python is used (Django must be installed in your active env).
    command: process.env.CI
      ? '..\\venv\\Scripts\\python ..\\ymgportal\\manage.py runserver 127.0.0.1:8000 --noreload --nothreading'
      : 'python ..\\ymgportal\\manage.py runserver 127.0.0.1:8000 --noreload --nothreading',
    url: 'http://127.0.0.1:8000',
    timeout: 120000,
    reuseExistingServer: !process.env.CI,
  },
});
