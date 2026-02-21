const { test, expect } = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const users = require('../../testData/users.json');

test('Employee Login test', async ({ page }) => {
  const login = new LoginPage(page);

  await login.open();
  await login.login(users.employee.username, users.employee.password);

  await expect(page).toHaveURL('http://127.0.0.1:8000/employee_home/');
});