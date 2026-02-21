function generateEmployee() {
  const unique = Date.now();

  return {
    id: `EMP${unique}`,
    name: `AutoUser${unique}`,
    email: `auto${unique}@test.com`,
    dob: '2000-02-20',
    phone: '9876543210',
    customer: 'Robert',
    designation: 'QA Engineer',
    roleSow: 'johndoe',
    dateOfJoining: '2025-02-20',
    sowStartDate: '2026-01-20',
    sowEndDate: '2026-02-20',
    otAllowed: false,
    phAllowed: false,
    country: 'India'
  };
}

module.exports = { generateEmployee };
