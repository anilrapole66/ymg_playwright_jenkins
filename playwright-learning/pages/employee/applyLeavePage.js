class ApplyLeavePage {
  constructor(page) {
    this.page = page;

    // this.leaveType = page.locator('select[name="leave_type"]');
    this.leaveType = page.locator('#id_leave_type');

    this.startDate = page.locator('input[name="start_date"]');
    this.endDate = page.locator('input[name="end_date"]');
    this.reason = page.locator('textarea[name="reason"]');

    this.submitBtn = page.getByRole('button', { name: 'Submit' });
  }

  async applyLeave(data) {

    // dropdown
    await this.leaveType.selectOption(data.type);

    // date fields (HTML date inputs expect yyyy-mm-dd)
    await this.startDate.fill(data.startDate);
    await this.endDate.fill(data.endDate);

    // textarea
    await this.reason.fill(data.reason);

    // submit
    await this.submitBtn.click();
  }
}

module.exports = ApplyLeavePage;
