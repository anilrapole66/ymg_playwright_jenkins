const { test, expect } = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const credentials = require('../../utils/credentials');
const EmployeeProfilePage = require('../../pages/employee/employeeProfilePage');
const LeaveDetailsPage = require('../../pages/employee/leaveDetailsPage');
const ApplyLeavePage = require('../../pages/employee/applyLeavePage');

test.use({ storageState: undefined });

test('Employee apply leave', async ({ page }) => {
  const login = new LoginPage(page);
  const empProfile = new EmployeeProfilePage(page);
  const leaveDetails = new LeaveDetailsPage(page);
  const leave = new ApplyLeavePage(page);

  await login.open();
  await login.login(credentials.employee.username, credentials.employee.password);

  await empProfile.openMenu();
  await empProfile.leaveDetails();

  await leaveDetails.goToapplyLeave();

  await leave.applyLeave({
    type: 'medical Leave',
    startDate: '2026-03-10',
    endDate: '2026-03-12',
    reason: 'Medical appointment',
  });
});
