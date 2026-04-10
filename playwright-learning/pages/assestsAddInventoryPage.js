class AssetAddInventoryPage {
  constructor(page) {
    this.page = page;

    this.assetType = page.locator('input[name="asset_type"]');
    this.assetColor = page.locator('input[name="asset_color"]');
    this.serialNumber = page.locator('input[name="serial_number"]');
    this.purchasedAt = page.locator('input[name="purchased_at"]');
    this.purchasedDate = page.locator('input[name="purchased_date"]');
    this.lastRepairedOn = page.locator('input[name="last_repaired_on"]');
    this.description = page.locator('textarea[name="optional_description"]');
    this.lastRepairDetails = page.locator('textarea[name="last_repair_details"]');
    this.isActive = page.getByRole('checkbox', { name: 'Active' });
    this.save = page.getByRole('button', { name: 'Save' });
  }

  async addAssetInventory(data) {
    await this.assetType.fill(data.assetType);
    await this.assetColor.fill(data.assetColor);
    await this.serialNumber.fill(data.serialNumber);
    await this.purchasedAt.fill(data.purchasedAt);
    await this.purchasedDate.fill(data.purchasedDate);
    await this.lastRepairedOn.fill(data.lastRepairedOn);
    await this.description.fill(data.description);
    await this.lastRepairDetails.fill(data.lastRepairDetails);

    if (data.isActive) {
      await this.isActive.check();
    } else {
      await this.isActive.uncheck();
    }

    await this.save.click();
  }
}

module.exports = AssetAddInventoryPage;
