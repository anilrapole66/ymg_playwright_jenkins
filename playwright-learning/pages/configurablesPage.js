class ConfigurablesPage {
  constructor(page) {
    this.page = page;

    this.clientBtn = page.getByText('Clients');
    this.addClientBtn = page.getByRole('link', { name: 'Add Client' });
    this.roleSowBtn = page.locator('.config-item', { hasText: 'SOW Roles' });
    this.addRoleSowBtn = page.getByRole('link', { name: 'Add SOW Role' });
  }

  async openClient() {
    await this.clientBtn.click();
  }

  async addClient() {
    await this.addClientBtn.click();
    await this.page.waitForURL(/add-main-client/);
  }

  async openRoleSow() {
    await this.roleSowBtn.click();
  }

  async addRoleSow() {
    await this.addRoleSowBtn.click();
    await this.page.waitForURL(/add/);
  }
}

module.exports = ConfigurablesPage;
