const { test, expect } = require('./baseTest');
const LoginPage = require('../pages/loginPage');
const credentials = require('../utils/credentials');

// Fresh unauthenticated context — storageState must not apply for login tests
test.use({ storageState: undefined });

test('Login test', async ({ page }) => {
  const login = new LoginPage(page);

  await login.open();
  await login.login(credentials.admin.username, credentials.admin.password);

  await expect(page).toHaveURL(/employee_list/);
});
