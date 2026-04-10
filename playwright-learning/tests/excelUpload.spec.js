const { test, expect } = require('./baseTest');
const EmployeePage = require('../pages/employeePage');
const ExcelUpload = require('../pages/excelUpload');

test('Upload employees using excel', async ({ page }) => {
  const employee = new EmployeePage(page);
  const upload = new ExcelUpload(page);

  await page.goto('/employee_list/');
  await employee.openAddEmployeeForm();
  await employee.goToUploadEmployees();

  await expect(page).toHaveURL(/upload-employees/);

  await upload.uploadFile('testData/employee_uploader_template.xlsx');
});
