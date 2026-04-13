const path = require('path');
const fs = require('fs');

/**
 * Reads the dropdown values that globalSetup scraped from the live app.
 * Falls back to safe defaults if the file doesn't exist yet
 * (e.g. running a single test file before globalSetup has run).
 */
function loadDropdowns() {
  const dropdownsPath = path.join(__dirname, '../playwright/.auth/dropdowns.json');
  if (fs.existsSync(dropdownsPath)) {
    return JSON.parse(fs.readFileSync(dropdownsPath, 'utf8'));
  }
  console.warn('[testData] dropdowns.json not found — using fallback values. Run full suite first.');
  return { customers: ['Robert'], roleSows: ['johndoe'], leaveTypes: [] };
}

function generateEmployee() {
  const unique = Date.now();
  const { customers, roleSows } = loadDropdowns();

  if (!customers.length) {
    throw new Error(
      '[testData] No customers found in dropdowns.json.\n' +
      'Make sure at least one MainClient exists in the database before running tests.\n' +
      'Run: python manage.py seed_ci'
    );
  }

  return {
    id:            `EMP${unique}`,
    name:          `AutoUser${unique}`,
    email:         `auto${unique}@test.com`,
    dob:           '2000-02-20',
    phone:         '9876543210',
    customer:      customers[0],
    designation:   'QA Engineer',
    roleSow:       roleSows[0] || null,
    dateOfJoining: '2025-02-20',
    sowStartDate:  '2026-01-20',
    sowEndDate:    '2026-02-20',
    otAllowed:     false,
    phAllowed:     false,
    country:       'India',
  };
}

function generateLeave() {
  const { leaveTypes } = loadDropdowns();

  if (!leaveTypes.length) {
    throw new Error(
      '[testData] No leave types found in dropdowns.json.\n' +
      'Make sure LeaveType records exist in the database before running tests.'
    );
  }

  return {
    type:      leaveTypes[0],       // first real leave type from the live DB
    startDate: '2026-03-10',
    endDate:   '2026-03-12',
    reason:    'Automation test leave request',
  };
}

module.exports = { generateEmployee, generateLeave, loadDropdowns };
