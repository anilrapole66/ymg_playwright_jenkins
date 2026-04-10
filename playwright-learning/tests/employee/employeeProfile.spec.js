const { test, expect } = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const credentials = require('../../utils/credentials');
const EmployeeProfilePage = require('../../pages/employee/employeeProfilePage');

test.use({ storageState: undefined });

test('Employee profile navigation', async ({ page }) => {
  const login = new LoginPage(page);
  const empProfile = new EmployeeProfilePage(page);

  await login.open();
  await login.login(credentials.employee.username, credentials.employee.password);

  await empProfile.openMenu();
});
