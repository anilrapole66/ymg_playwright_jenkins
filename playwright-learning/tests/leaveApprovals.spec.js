const { test, expect } = require('./baseTest');
const EmployeePage = require('../pages/employeePage');
const LeaveApprovalPage = require('../pages/leaveApprovalPage');

test('Leave Approvals', async ({ page }) => {
  const emp = new EmployeePage(page);
  const leaveApprove = new LeaveApprovalPage(page);

  await page.goto('/employee_list/');
  await emp.goToLeaveApprovals();
  await leaveApprove.goToLeaveApprove();
});
