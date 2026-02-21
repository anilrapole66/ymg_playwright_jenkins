class LogoutPage {
  constructor(page) {
    this.page = page;
    this.logoutBtn = page.getByRole('button', { name: 'Logout' });
  }

  async logout() {
    await this.logoutBtn.click();
  }
}

module.exports = LogoutPage;
