const { test } = require('@playwright/test');
const EmployeeProfilePage = require('../../pages/employee/employeeProfilePage');
const ClaimDetailsPage = require('../../pages/employee/claimsDetailPage');
const NewClaimPage = require('../../pages/employee/newClaimPage');

test('Employee new claim flow', async ({ page }) => {
  const empProfile = new EmployeeProfilePage(page);
  const claims = new ClaimDetailsPage(page);
  const newClaim = new NewClaimPage(page);

  // No manual login — employee storageState is injected by the 'employee' project
  await page.goto('/employee_home/');
  await page.waitForURL(/employee_home/, { timeout: 10000 });

  await empProfile.openMenu();
  await empProfile.claims();

  await claims.newClaim();

  await newClaim.submitClaim({
    startDate: '2026-02-15',
    endDate: '2026-02-16',
    description: 'Travel reimbursement',
    amount: '250',
    filePath: 'testData/backpackhover.jpg',
  });
});
