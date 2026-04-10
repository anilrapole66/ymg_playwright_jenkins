const { test, expect } = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const LogoutPage = require('../../pages/logoutPage');
const credentials = require('../../utils/credentials');

test.use({ storageState: undefined });

test('Employee Logout flow', async ({ page }) => {
  const login = new LoginPage(page);
  const logout = new LogoutPage(page);

  await login.open();
  await login.login(credentials.employee.username, credentials.employee.password);

  await logout.logout();

  await expect(page).toHaveURL(/\/login\//);
});
