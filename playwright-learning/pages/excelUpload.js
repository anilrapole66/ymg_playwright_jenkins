class excelUpload {
  constructor(page) {
    this.page = page;

    // upload page elements
    this.fileInput = page.locator('input[type="file"]');
    this.submitBtn = page.getByRole('button', { name: /submit|upload/i });
    this.successMsg = page.locator('text=success');
  }

  async uploadFile(filePath) {
    await this.fileInput.setInputFiles(filePath);
    await this.submitBtn.click();
  }
}

module.exports = excelUpload;
