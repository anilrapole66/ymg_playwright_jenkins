class AssestAddInventoryPage{
   constructor(page) {
    this.page = page;

    this.assestType = page.locator('input[name="asset_type"]');
    this.assestColor = page.locator('input[name="asset_color"]');
    this.serialNumber = page.locator('input[name="serial_number"]');
    this.purchasedAt = page.locator('input[name="purchased_at"]');
    this.purchasedDate =page.locator('input[name="purchased_date"]');
    this.lastRepairedOn =page.locator('input[name="last_repaired_on"]');
    this.description = page.locator('textarea[name="optional_description"]');
    this.lastRepairDetails = page.locator('textarea[name="last_repair_details"]');
    this.isActive = page.getByRole('checkbox',{name:'Active'})

    this.save = page.getByRole('button', { name: 'Save' });
  }

  async addAssestInventory(data) {

    await this.assestType.fill(data.assestType);
    await this.assestColor.fill(data.assestColor);
    await this.serialNumber.fill(data.serialNumber);
    await this.purchasedAt.fill(data.purchasedAt);
    await this.purchasedDate.fill( data.purchasedDate );
    await this.lastRepairedOn.fill( data.lastRepairedOn );
    await this.description.fill(data.description);
    await this.lastRepairDetails.fill(data.lastRepairDetails);

    if (data.active)
      await this.isActive.check();
    else
      await this.isActive.uncheck();

    await this.save.click();
    
  }
}

module.exports = AssestAddInventoryPage;