const { test, expect } = require('../tests/fixtures/testBase');
const LoginPage = require('../pages/loginPage');
const ConfigurablesPage = require('../pages/configurablesPage');
const AddClientPage = require('../pages/clientPage');
const { generateClient } = require('../utils/clientData');
const EmployeePage = require('../pages/employeePage');
const users = require('../testData/users.json');

test('Add client flow', async ({ page }) => {

  const login = new LoginPage(page);
  const employee = new EmployeePage(page);
  const config = new ConfigurablesPage(page);
  const addClient = new AddClientPage(page);

  const client = generateClient();

  await login.open();
  await login.login(users.admin.username, users.admin.password);

  // employee_list → configurables
  await employee.openConfigurables();

  // configurables → add client
  await config.openClient();

  await config.addClient();

  // add client
  await addClient.addClient(client);

  // verify client visible
//   await expect(page.getByText(client.name)).toBeVisible();

  // store for cleanup
  test.info().annotations.push({
    type: 'clientName',
    description: client.name
  });
});
