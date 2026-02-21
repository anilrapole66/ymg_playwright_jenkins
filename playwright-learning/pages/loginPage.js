class LoginPage {
  constructor(page) {
    this.page = page;
    this.username = page.locator('#username');
    this.password = page.locator('#password');
    this.loginBtn = page.getByRole('button', { name: 'Login' });
  }

  async open() {
    await this.page.goto('http://127.0.0.1:8000/login/');
  }

  async login(username, password) {
    await this.username.fill(username);
    await this.password.fill(password);
    await this.loginBtn.click();
  }
}

module.exports = LoginPage;
