const { test } = require('@playwright/test');
const EmployeeProfilePage = require('../../pages/employee/employeeProfilePage');
const LeaveDetailsPage = require('../../pages/employee/leaveDetailsPage');
const ApplyLeavePage = require('../../pages/employee/applyLeavePage');
const { generateLeave } = require('../../utils/testData');

test('Employee apply leave', async ({ page }) => {
  const leaveData = generateLeave();

  const empProfile = new EmployeeProfilePage(page);
  const leaveDetails = new LeaveDetailsPage(page);
  const leave = new ApplyLeavePage(page);

  // No manual login — employee storageState is injected by the 'employee' project
  await page.goto('/employee_home/');

  await empProfile.openMenu();
  await empProfile.leaveDetails();

  await leaveDetails.goToapplyLeave();

  await leave.applyLeave(leaveData);
});
