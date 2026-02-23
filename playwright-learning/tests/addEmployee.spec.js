const { test, expect } = require('../tests/fixtures/testBase');
const LoginPage = require('../pages/loginPage');
const EmployeePage = require('../pages/employeePage');
const { generateEmployee } = require('../utils/testData');
const users = require('../testData/users.json');

test('Add Employee flow', async ({ page }) => {

  const login = new LoginPage(page);
  const employee = new EmployeePage(page);
  const empData = generateEmployee();

  // login
  await login.open();
  await login.login(users.admin.username, users.admin.password);

  // ensure employee list page opened
  await expect(page).toHaveURL(/employee_list/);

  // open add employee page
  await employee.openAddEmployeeForm();
  await employee.addEmployee(empData);

  // ⭐ store id for cleanup
  test.info().annotations.push({
    type: 'employeeId',
    description: empData.id
  });

  // verify redirected back
  await expect(page).toHaveURL(/employee_list/);
});
