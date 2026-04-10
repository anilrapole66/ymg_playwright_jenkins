const { test, expect } = require('./baseTest');
const ConfigurablesPage = require('../pages/configurablesPage');
const AddRoleSowPage = require('../pages/roleSowPage');
const { generateRoleSow } = require('../utils/roleSowData');
const EmployeePage = require('../pages/employeePage');

test('Add RoleSow flow', async ({ page }) => {
  const employee = new EmployeePage(page);
  const config = new ConfigurablesPage(page);
  const addRoleSow = new AddRoleSowPage(page);

  const roleSow = generateRoleSow();

  await page.goto('/employee_list/');
  await employee.openConfigurables();
  await config.openRoleSow();
  await config.addRoleSow();
  await addRoleSow.addRoleSow(roleSow);

  await expect(page).toHaveURL(/configurables/);
});
