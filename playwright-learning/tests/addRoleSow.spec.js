const { test, expect } = require('./baseTest');
const LoginPage = require('../pages/loginPage');
const ConfigurablesPage = require('../pages/configurablesPage');
const AddRoleSowPage = require('../pages/roleSowPage');
const { generateRoleSow } = require('../utils/roleSowData');
const EmployeePage = require('../pages/employeePage');
const users = require('../testData/users.json');

test('Add ROleSow flow', async ({ page }) => {

  const login = new LoginPage(page);
  const employee = new EmployeePage(page);
  const config = new ConfigurablesPage(page);
  const addRoleSow = new AddRoleSowPage(page);

  const roleSow = generateRoleSow();

  await login.open();
  await login.login(users.admin.username, users.admin.password);

  // employee_list → configurables
  await employee.openConfigurables();

  // configurables → add client
  await config.openRoleSow();

  await config.addRoleSow();

  // add client
  await addRoleSow.addRoleSow(roleSow);

  // verify client visible
//   await expect(page.getByText(client.name)).toBeVisible();

  // store for cleanup
  // test.info().annotations.push({
  //   type: 'clientName',
  //   description: client.name
  // });
});
