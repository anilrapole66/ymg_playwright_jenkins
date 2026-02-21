const {test, expect} = require('@playwright/test');
const LoginPage = require('../../pages/loginPage');
const users = require('../../testData/users.json');
const EmployeeProfilePage = require('../../pages/employee/employeeProfilePage');
const ClaimDetailsPage = require('../../pages/employee/claimsDetailPage');
const NewClaimPage = require('../../pages/employee/newClaimPage');

test ('New Claim Flow', async({page}) => {
    const login = new LoginPage(page);
    const empProfile = new EmployeeProfilePage(page);
    const claims = new ClaimDetailsPage(page);
    const newClaim = new NewClaimPage(page);

       await login.open();
       await login.login(users.employee.username, users.employee.password);

       await empProfile.openMenu();
       await empProfile.claims();

       await claims.newClaim();

       await newClaim.submitClaim({
        startDate: '2026-02-15',
        endDate: '2026-02-16',
        description: 'Travel reimbursement',
        amount: '250',
        filePath: 'testData/backpackhover.jpg'
  });






});
