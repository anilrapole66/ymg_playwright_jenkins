const { test, expect } = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const users = require('../../testData/users.json');
const EmployeeProfilePage = require('../../pages/employee/employeeProfilePage');

test('employee', async ({ page }) => {

  const login = new LoginPage(page);
  const empProfile = new EmployeeProfilePage(page);

  await login.open();
  await login.login(users.employee.username, users.employee.password);

  await empProfile.openMenu();
  
});