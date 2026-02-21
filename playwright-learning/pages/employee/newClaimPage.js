class NewClaimPage{
    constructor(page){
    this.page =page;
        
    this.startDate = page.locator('input[name="start_date"]');
    this.endDate = page.locator('input[name="end_date"]');
    this.description = page.locator('textarea[name="description"]');
    this.amount = page.locator('input[name="amount"]');
    this.fileInput = page.locator('input[name="file"]');
    this.submitBtn = page.getByRole('button', { name: 'Submit Claim' });
    }

    async submitClaim(data){

    await this.startDate.fill(data.startDate);
    await this.endDate.fill(data.endDate);
    await this.description.fill(data.description);
    await this.amount.fill(data.amount);

    // Upload file
    await this.fileInput.setInputFiles(data.filePath);

    await this.submitBtn.click();
    }
}
module.exports = NewClaimPage;