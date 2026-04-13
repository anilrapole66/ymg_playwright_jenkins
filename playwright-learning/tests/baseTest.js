const base = require('@playwright/test');
const EmployeePage = require('../pages/employeePage');

/**
 * Extended test with shared afterEach cleanup.
 * Auth state is loaded via storageState so every test context
 * starts pre-authenticated as admin.
 */
const test = base.test.extend({});

test.afterEach(async ({ page }, testInfo) => {
  const employee = new EmployeePage(page);

  const empId    = testInfo.annotations.find(a => a.type === 'employeeId');
  const client   = testInfo.annotations.find(a => a.type === 'clientName');
  const roleSow  = testInfo.annotations.find(a => a.type === 'roleSowName');

  if (!empId && !client && !roleSow) return;

  if (empId) {
    try { await employee.deleteEmployee(empId.description); }
    catch (err) { console.log('Employee cleanup skipped:', err.message); }
  }

  if (client) {
    try { await employee.deleteCustomer(client.description); }
    catch (err) { console.log('Client cleanup skipped:', err.message); }
  }

  if (roleSow) {
    try { await employee.deleteRoleSow(roleSow.description); }
    catch (err) { console.log('RoleSow cleanup skipped:', err.message); }
  }
});

module.exports = { test, expect: base.expect };
