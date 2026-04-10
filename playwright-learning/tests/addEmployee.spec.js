const { test, expect } = require('./baseTest');
const EmployeePage = require('../pages/employeePage');
const { generateEmployee } = require('../utils/testData');

test('Add Employee flow', async ({ page }) => {
  const employee = new EmployeePage(page);
  const empData = generateEmployee();

  await page.goto('/employee_list/');
  await expect(page).toHaveURL(/employee_list/);

  await employee.openAddEmployeeForm();
  await employee.addEmployee(empData);

  test.info().annotations.push({ type: 'employeeId', description: empData.id });

  await expect(page).toHaveURL(/employee_list/);
});
