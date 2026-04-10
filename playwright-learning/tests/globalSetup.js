const { chromium } = require('@playwright/test');
const credentials = require('../utils/credentials');
const path = require('path');
const fs = require('fs');

/**
 * Runs once before all tests.
 * Logs in with admin credentials and saves the auth state so every
 * test context starts already authenticated — no per-test login needed.
 *
 * Playwright starts the webServer (Django dev server) before this runs,
 * so the login URL is already available.
 */
module.exports = async function globalSetup(config) {
  const baseURL = config.use?.baseURL || 'http://127.0.0.1:8000';
  const authDir = path.join(__dirname, '../playwright/.auth');
  fs.mkdirSync(authDir, { recursive: true });

  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto(`${baseURL}/login/`);
  await page.locator('#username').fill(credentials.admin.username);
  await page.locator('#password').fill(credentials.admin.password);
  await page.getByRole('button', { name: 'Login' }).click();
  await page.waitForURL(/employee_list/);

  await context.storageState({ path: path.join(authDir, 'admin.json') });
  await browser.close();
};
