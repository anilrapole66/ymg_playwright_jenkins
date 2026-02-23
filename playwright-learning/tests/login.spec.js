const { test, expect } = require('../fixtures/testBase');
const LoginPage = require('../pages/loginPage');
const users = require('../testData/users.json');

test('Login test', async ({ page }) => {
  const login = new LoginPage(page);

  await login.open();
  await login.login(users.admin.username, users.admin.password);

  await expect(page).toHaveURL('http://127.0.0.1:8000/employee_list/');
});
