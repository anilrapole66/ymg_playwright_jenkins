const path = require('path');
const fs = require('fs');

function loadDropdowns() {
  const dropdownsPath = path.join(__dirname, '../playwright/.auth/dropdowns.json');
  if (fs.existsSync(dropdownsPath)) {
    return JSON.parse(fs.readFileSync(dropdownsPath, 'utf8'));
  }
  console.warn('[roleSowData] dropdowns.json not found — using fallback values. Run full suite first.');
  return { customers: ['Robert'], roleSows: ['johndoe'] };
}

function generateRoleSow() {
  const unique = Date.now();
  const { customers } = loadDropdowns();

  return {
    name:        `AUTO_ROLE_${unique}`,
    description: `AUTO_DESC_${unique}`,
    mainClient:  customers[0],   // first real client from the live DB
  };
}

module.exports = { generateRoleSow };
