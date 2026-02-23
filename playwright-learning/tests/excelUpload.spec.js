const { test, expect } = require('./baseTest');
const LoginPage = require('../pages/loginPage');
const EmployeePage = require('../pages/employeePage');
const excelUpload = require('../pages/excelUpload');
const users = require('../testData/users.json');

test('Upload employees using excel', async ({ page }) => {

  const login = new LoginPage(page);
  const employee = new EmployeePage(page);
  const upload = new excelUpload(page);

  // login
  await login.open();
  await login.login(users.admin.username, users.admin.password);

  // employee list → add employee
  await employee.openAddEmployeeForm();

  // add employee → upload excel page
  await employee.goToUploadEmployees();

  // verify page opened
  await expect(page).toHaveURL(/upload-employees/);

  // upload file
  await upload.uploadFile('testData/employee_uploader_template.xlsx');

});
