const { test, expect } = require('./baseTest');
const LoginPage = require('../pages/loginPage');
const EmployeePage = require('../pages/employeePage'); 
const LeaveApprovalPage = require('../pages/leaveApprovalPage');
const users = require('../testData/users.json');

test('Leave Approvals', async ({ page }) => {

  const login = new LoginPage(page);
  const emp = new EmployeePage(page);
  const leaveApprove = new LeaveApprovalPage(page);

  await login.open();
  await login.login(users.admin.username, users.admin.password);

  await emp.goToLeaveApprovals();

  await leaveApprove.goToLeaveApprove();

  });