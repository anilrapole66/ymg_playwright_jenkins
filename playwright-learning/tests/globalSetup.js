const { chromium } = require('@playwright/test');
const credentials = require('../utils/credentials');
const path = require('path');
const fs = require('fs');

module.exports = async function globalSetup(config) {
  const baseURL = config.use?.baseURL || 'http://127.0.0.1:8000';
  const authDir = path.join(__dirname, '../playwright/.auth');
  fs.mkdirSync(authDir, { recursive: true });

  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // ── 1. Login ────────────────────────────────────────────────────────────────
  await page.goto(`${baseURL}/login/`);
  await page.locator('#username').fill(credentials.admin.username);
  await page.locator('#password').fill(credentials.admin.password);
  await page.getByRole('button', { name: 'Login' }).click();
  await page.waitForURL(/employee_list/);

  await context.storageState({ path: path.join(authDir, 'admin.json') });

  // ── 2. Scrape dropdowns ─────────────────────────────────────────────────────
  // Helper: read non-blank <option> text contents from a CSS selector
  async function scrapeOptions(selector) {
    const texts = await page
      .locator(`${selector} option:not([value=""])`)
      .allTextContents()
      .catch(() => []);
    return texts.map(t => t.trim()).filter(Boolean);
  }

  // --- add-employee form: Customer + RoleSow ---
  await page.goto(`${baseURL}/add-employee/`);
  await page.waitForLoadState('domcontentloaded');
  const customers = await scrapeOptions('select[name="main_account"]');
  const roleSows  = await scrapeOptions('select[name="role_sow"]');

  // --- leave apply form: LeaveType ---
  // Admin has no Employee profile so /leave-apply/ never renders the form for admin.
  // Use a separate employee context to scrape the leave type dropdown.
  // These are the same values that seed_ci.py always seeds — used as fallback.
  const SEEDED_LEAVE_TYPES = ['Annual Leave', 'Medical Leave', 'Unpaid Leave'];
  let leaveTypes = [];
  const empUsername = credentials.employee?.username;
  const empPassword = credentials.employee?.password;

  if (empUsername && empPassword) {
    const empContext = await browser.newContext();
    const empPage = await empContext.newPage();

    await empPage.goto(`${baseURL}/login/`);
    await empPage.locator('#username').fill(empUsername);
    await empPage.locator('#password').fill(empPassword);
    await empPage.getByRole('button', { name: 'Login' }).click();
    await empPage.waitForLoadState('domcontentloaded');

    const afterLoginURL = empPage.url();
    console.log(`[globalSetup] employee login → ${afterLoginURL}`);

    if (afterLoginURL.includes('/login/')) {
      console.warn(`[globalSetup] Employee login failed — still on login page. Check credentials for: ${empUsername}`);
    } else {
      // Save employee auth state for the employee project
      await empContext.storageState({ path: path.join(authDir, 'employee.json') });
      console.log('[globalSetup] Saved employee.json');
      await empPage.goto(`${baseURL}/leave-apply/`);
      await empPage.waitForLoadState('domcontentloaded');

      const leavePageURL = empPage.url();
      console.log(`[globalSetup] leave-apply page → ${leavePageURL}`);

      const formVisible = await empPage.locator('#id_leave_type').isVisible({ timeout: 5000 }).catch(() => false);
      console.log(`[globalSetup] #id_leave_type visible: ${formVisible}`);

      if (formVisible) {
        // Wait for at least one real option to be present before reading
        await empPage.locator('#id_leave_type option:not([value=""])').first().waitFor({ timeout: 5000 }).catch(() => {});
        const texts = await empPage
          .locator('#id_leave_type option:not([value=""])')
          .allTextContents()
          .catch(() => []);
        leaveTypes = texts.map(t => t.trim()).filter(Boolean);
      } else {
        const bodyText = await empPage.locator('body').innerText().catch(() => '');
        console.warn(`[globalSetup] /leave-apply/ did not render the form. Page text (first 300 chars): ${bodyText.slice(0, 300)}`);
      }
    }

    await empContext.close();
  } else {
    console.warn('[globalSetup] TEST_EMPLOYEE_USER not set — skipping leaveTypes scrape.');
  }

  // Fall back to seeded defaults if UI scraping returned nothing
  if (leaveTypes.length === 0) {
    leaveTypes = SEEDED_LEAVE_TYPES;
    console.warn(`[globalSetup] leaveTypes scraped 0 — using seeded defaults: ${leaveTypes.join(', ')}`);
  }

  const dropdowns = { customers, roleSows, leaveTypes };

  fs.writeFileSync(
    path.join(authDir, 'dropdowns.json'),
    JSON.stringify(dropdowns, null, 2)
  );

  console.log(`\n[globalSetup] customers  (${dropdowns.customers.length}): ${dropdowns.customers.join(', ')}`);
  console.log(`[globalSetup] roleSows   (${dropdowns.roleSows.length}): ${dropdowns.roleSows.join(', ')}`);
  console.log(`[globalSetup] leaveTypes (${dropdowns.leaveTypes.length}): ${dropdowns.leaveTypes.join(', ')}\n`);

  await browser.close();
};
