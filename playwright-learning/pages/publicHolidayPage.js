class PublicHolidayPage {
  constructor(page) {
    this.page = page;

    this.holidayName = page.getByRole('textbox', {name:'Holiday name'});
    this.holidayDate = page.getByLabel('Holiday date');
    this.country = page.getByRole('combobox', {name:'Country'});
    this.description = page.getByRole('textbox', {name:'Description'});
    this.isActive = page.getByLabel('Is active');
    this.saveBtn = page.getByRole('button', { name: 'Save' });
  }

  async addHoliday(data) {

    await this.holidayName.fill(data.name);

    // HTML5 date input (no calendar clicking needed)
    await this.holidayDate.fill(data.date);

    await this.country.selectOption(data.country);

    await this.description.fill(data.description);

    if (data.active)
      await this.isActive.check();
    else
      await this.isActive.uncheck();

    await this.saveBtn.click();
  }
}

module.exports = PublicHolidayPage;
