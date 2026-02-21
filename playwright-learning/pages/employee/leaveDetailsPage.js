class LeaveDetailsPage {
    constructor(page){
        this.page= page;
        this.applyleaveBtn = page.getByRole('link', { name: '＋ Apply Leave' });

      }

    async goToapplyLeave() {
       await this.applyleaveBtn.click();
    //    await this.page.waitForUrl(/leave-apply/);
    
  }
}
module.exports = LeaveDetailsPage;