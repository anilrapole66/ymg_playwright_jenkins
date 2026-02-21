class roleSowPage {
  constructor(page) {
    this.page = page;

    this.roleSowName = page.getByRole('textbox', { name: 'Name'});
    this.description = page.getByRole('textbox', { name: 'Description'});
    this.mainClient = page.getByRole('combobox', { name: 'Main Client'}); 
    // getByLabel('Main Client:').selectOption('1');

    this.addRoleBtn = page.getByRole('button', { name: 'Add Role' });
  }

  async addRoleSow(data) {

    await this.roleSowName.fill(data.name);
    await this.description.fill(data.description);
    await this.mainClient.selectOption({ label: data.mainClient });
    await this.addRoleBtn.click();
    
  }
}

module.exports = roleSowPage;
