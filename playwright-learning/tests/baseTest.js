const base = require('@playwright/test');
const EmployeePage = require('../pages/employeePage');

/**
 * Extended test with shared afterEach cleanup.
 * Auth state is loaded via storageState (set in playwright.config.js),
 * so no explicit login is needed in cleanup.
 */
const test = base.test.extend({});

test.afterEach(async ({ page }, testInfo) => {
  try {
    const empId = testInfo.annotations.find(a => a.type === 'employeeId');
    if (!empId) return;

    const employee = new EmployeePage(page);
    await employee.deleteEmployee(empId.description);

    const client = testInfo.annotations.find(a => a.type === 'clientName');
    if (client) {
      await employee.deleteCustomer(client.description);
    }
  } catch (err) {
    console.log('Cleanup skipped:', err.message);
  }
});

module.exports = { test, expect: base.expect };
