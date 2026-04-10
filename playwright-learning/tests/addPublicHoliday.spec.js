const { test, expect } = require('./baseTest');
const EmployeePage = require('../pages/employeePage');
const PublicHolidayPage = require('../pages/publicHolidayPage');

test('Add Public Holiday', async ({ page }) => {
  const emp = new EmployeePage(page);
  const holiday = new PublicHolidayPage(page);

  await page.goto('/employee_list/');
  await emp.goToPublicHoliday();
  await emp.addPublicHoliday();

  await holiday.addHoliday({
    name: 'newyear',
    date: '2026-01-26',
    country: 'India',
    description: 'Automation Test Holiday',
    active: true,
  });
});
