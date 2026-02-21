class EmployeeProfilePage {
    constructor(page){
        this.page= page;
        this.menuBtn = page.locator('#menuToggle');
        this.leavedetailsBtn = page.getByRole('link',{name:'Leave Details'});
        this.claimsBtn = page.getByRole('link',{name:'Claims'});
      
      }

    async openMenu() {
       await this.menuBtn.click();
   }

    async leaveDetails() {
      await this.leavedetailsBtn.click();
      await this.page.waitForURL(/employee\/\d+\/leaves\//);
    }

    async claims(){
      await this.claimsBtn.click();
      await this.page.waitForURL(/claims/);
    }
}
module.exports = EmployeeProfilePage;