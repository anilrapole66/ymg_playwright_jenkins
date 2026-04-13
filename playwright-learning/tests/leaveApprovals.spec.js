const { test } = require('./baseTest');
const EmployeePage = require('../pages/employeePage');
const LeaveApprovalPage = require('../pages/leaveApprovalPage');

test('Leave Approvals', async ({ page }) => {
  const emp = new EmployeePage(page);
  const leaveApprove = new LeaveApprovalPage(page);

  await page.goto('/employee_list/');
  await emp.goToLeaveApprovals();

  const approved = await leaveApprove.goToLeaveApprove();
  test.info().annotations.push({
    type: 'result',
    description: approved ? 'Leave request approved' : 'No pending leaves — nothing to approve',
  });
});
