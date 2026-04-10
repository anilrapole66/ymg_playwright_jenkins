const { test, expect } = require('./baseTest');
const LoginPage = require('../pages/loginPage');
const LogoutPage = require('../pages/logoutPage');
const credentials = require('../utils/credentials');

// Fresh unauthenticated context so we can test the full login → logout flow
test.use({ storageState: undefined });

test('Logout flow', async ({ page }) => {
  const login = new LoginPage(page);
  const logout = new LogoutPage(page);

  await login.open();
  await login.login(credentials.admin.username, credentials.admin.password);

  await logout.logout();

  await expect(page).toHaveURL(/\/login\//);
});
