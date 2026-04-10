const { test, expect } = require('./baseTest');
const EmployeePage = require('../pages/employeePage');
const AssetAddInventoryPage = require('../pages/assestsAddInventoryPage');

test('Add Inventory Flow', async ({ page }) => {
  const emp = new EmployeePage(page);
  const asset = new AssetAddInventoryPage(page);

  await page.goto('/employee_list/');
  await emp.goToAssets();
  await emp.goToManageInventory();
  await emp.goToAddInventory();

  await asset.addAssetInventory({
    assetType: 'laptop',
    assetColor: 'black',
    serialNumber: '123',
    purchasedAt: 'store',
    purchasedDate: '2026-01-26',
    lastRepairedOn: '2025-01-26',
    description: 'Automation Test Asset',
    lastRepairDetails: 'color change',
    isActive: true,
  });
});
