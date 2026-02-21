class ClaimsDetailsPage{
    constructor(page){
        this.page = page;
        this.newClaimBtn = page.getByRole('link',{name:' + New Claim'});

    }

    async newClaim(){
            await this.newClaimBtn.click();
            await this.page.waitForURL(/submit/);
        }
}

module.exports = ClaimsDetailsPage;