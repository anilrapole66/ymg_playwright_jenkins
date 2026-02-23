const base = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const EmployeePage = require('../../pages/employeePage');

exports.test = base.test.extend({});

exports.expect = base.expect;

// ✅ SAFE place — inside Playwright test context
exports.test.afterEach(async ({ page }, testInfo) => {
  try {
    const empId = testInfo.annotations.find(a => a.type === 'employeeId');
    if (!empId) return;

    const login = new LoginPage(page);
    const employee = new EmployeePage(page);

    await login.open();
    await login.login('Anil', 'Anil@123');

    await employee.deleteEmployee(empId.description);

    const customer = testInfo.annotations.find(a => a.type === 'customerName');
    if (customer) {
      await employee.deletecustomer(customer.description);
    }

  } catch (err) {
    console.log('Cleanup skipped:', err.message);
  }
});