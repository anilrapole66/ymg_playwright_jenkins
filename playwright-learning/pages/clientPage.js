class ClientPage {
  constructor(page) {
    this.page = page;
    this.clientName = page.getByRole('textbox', { name: 'Name' });
    this.saveBtn = page.getByRole('button', { name: 'Save' });
  }

  async addClient(data) {
    await this.clientName.fill(data.name);
    await Promise.all([
      this.page.waitForURL(/configurables/),
      this.saveBtn.click(),
    ]);
  }
}

module.exports = ClientPage;
