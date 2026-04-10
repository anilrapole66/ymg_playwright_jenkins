/**
 * Loads test credentials from environment variables (CI/Jenkins) or
 * falls back to testData/users.json for local development.
 *
 * Jenkins credentials required:
 *   PLAYWRIGHT_ADMIN    — Username with password → TEST_ADMIN_USER / TEST_ADMIN_PASS
 *   PLAYWRIGHT_EMPLOYEE — Username with password → TEST_EMPLOYEE_USER / TEST_EMPLOYEE_PASS
 */
function loadCredentials() {
  const adminUser = process.env.TEST_ADMIN_USER;
  const adminPass = process.env.TEST_ADMIN_PASS;
  const empUser   = process.env.TEST_EMPLOYEE_USER;
  const empPass   = process.env.TEST_EMPLOYEE_PASS;

  if (adminUser && adminPass) {
    return {
      admin:    { username: adminUser, password: adminPass },
      employee: { username: empUser || '', password: empPass || '' },
    };
  }

  try {
    return require('../testData/users.json');
  } catch {
    throw new Error(
      'Test credentials not found.\n' +
      '  Option 1: set TEST_ADMIN_USER / TEST_ADMIN_PASS (and optionally TEST_EMPLOYEE_USER / TEST_EMPLOYEE_PASS).\n' +
      '  Option 2: copy testData/users.json.example to testData/users.json and fill in real values.'
    );
  }
}

module.exports = loadCredentials();
