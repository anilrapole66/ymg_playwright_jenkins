const { test, expect } = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const LogoutPage = require('../../pages/logoutPage');
const users = require('../../testData/users.json');

test('Logout flow', async ({ page }) => {

  const login = new LoginPage(page);
  const logout = new LogoutPage(page);

  // FIRST LOGIN
  await login.open();
  await login.login(users.employee.username, users.employee.password);

  // THEN LOGOUT
  await logout.logout();

  // VERIFY
  await expect(page).toHaveURL('http://127.0.0.1:8000/login/');
});
