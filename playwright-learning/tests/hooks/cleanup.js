const { test } = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const EmployeePage = require('../../pages/employeePage');

test.afterEach(async ({ page }, testInfo) => {

  const annotation = testInfo.annotations.find(a => a.type === 'employeeId');
  if (!annotation) return;

  const empId = annotation.description;

  const login = new LoginPage(page);
  const employee = new EmployeePage(page);

  // ensure logged in
  await login.open();
  await login.login('Anil', 'Anil@123');

  // delete created employee
  await employee.deleteEmployee(empId);

  console.log(`🧹 Cleaned employee: ${empId}`);
});
