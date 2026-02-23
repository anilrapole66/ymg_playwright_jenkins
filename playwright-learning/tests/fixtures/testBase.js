const base = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const EmployeePage = require('../../pages/employeePage');

// extend playwright test
const test = base.test.extend({});

test.afterEach(async ({ page }, testInfo) => {
  try {

    const empId = testInfo.annotations.find(a => a.type === 'employeeId');
    if (!empId) return;

    const login = new LoginPage(page);
    const employee = new EmployeePage(page);

    // login as admin
    await login.open();
    await login.login('Anil', 'Anil@123');

    // delete employee created in test
    await employee.deleteEmployee(empId.description);

    // delete customer if created
    const customer = testInfo.annotations.find(a => a.type === 'customerName');
    if (customer) {
      await employee.deletecustomer(customer.description);
    }

  } catch (err) {
    console.log('Cleanup skipped:', err.message);
  }
});

module.exports = { test, expect: base.expect };