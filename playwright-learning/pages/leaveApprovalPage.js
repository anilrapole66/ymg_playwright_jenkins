class LeaveApprovalsPage{
    constructor(page){
        this.page = page;
        this.leaveApproveBtn = page.getByRole('link',{name:'Approve'});
    }

    async goToLeaveApprove(){
        await this.leaveApproveBtn.click();
    }
}
module.exports = LeaveApprovalsPage
