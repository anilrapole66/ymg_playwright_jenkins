const { test, expect } = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const credentials = require('../../utils/credentials');

test.use({ storageState: undefined });

test('Employee Login test', async ({ page }) => {
  const login = new LoginPage(page);

  await login.open();
  await login.login(credentials.employee.username, credentials.employee.password);

  await expect(page).toHaveURL(/employee_home/);
});
