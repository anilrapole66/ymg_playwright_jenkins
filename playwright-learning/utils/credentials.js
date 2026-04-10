/**
 * Loads test credentials from environment variables (CI/Jenkins) or
 * falls back to testData/users.json for local development.
 *
 * In Jenkins, add a "Username with password" credential with ID
 * PLAYWRIGHT_ADMIN and inject it as TEST_ADMIN_USER / TEST_ADMIN_PASS.
 */
function loadCredentials() {
  const username = process.env.TEST_ADMIN_USER;
  const password = process.env.TEST_ADMIN_PASS;

  if (username && password) {
    return { admin: { username, password } };
  }

  try {
    return require('../testData/users.json');
  } catch {
    throw new Error(
      'Test credentials not found.\n' +
      '  Option 1: set TEST_ADMIN_USER and TEST_ADMIN_PASS environment variables.\n' +
      '  Option 2: copy testData/users.json.example to testData/users.json and fill in real values.'
    );
  }
}

module.exports = loadCredentials();
