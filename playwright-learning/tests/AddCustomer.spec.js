const { test, expect } = require('./baseTest');
const ConfigurablesPage = require('../pages/configurablesPage');
const ClientPage = require('../pages/clientPage');
const { generateClient } = require('../utils/clientData');
const EmployeePage = require('../pages/employeePage');

test('Add client flow', async ({ page }) => {
  const employee = new EmployeePage(page);
  const config = new ConfigurablesPage(page);
  const addClient = new ClientPage(page);

  const client = generateClient();

  await page.goto('/employee_list/');
  await employee.openConfigurables();
  await config.openClient();
  await config.addClient();
  await addClient.addClient(client);

  await expect(page).toHaveURL(/configurables/);

  test.info().annotations.push({ type: 'clientName', description: client.name });
});
