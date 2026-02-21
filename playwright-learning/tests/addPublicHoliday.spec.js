const { test, expect } = require('./baseTest');
const LoginPage = require('../pages/loginPage');
const EmployeePage = require('../pages/employeePage');
const PublicHolidayPage = require('../pages/publicHolidayPage');
const users = require('../testData/users.json');

test('Add Public Holiday', async ({ page }) => {

  const login = new LoginPage(page);
  const emp = new EmployeePage(page);
  const holiday = new PublicHolidayPage(page);

  await login.open();
  await login.login(users.admin.username, users.admin.password);

  await emp.goToPublicHoliday();

  await emp.AddPublicholiday();

  const holidayName = `Holiday-${Date.now()}`;

  await holiday.addHoliday({
    name: 'newyear',
    date: '2026-01-26',
    country: 'India',
    description: 'Automation Test Holiday',
    active: true
  });

});
