class LeaveApprovalsPage{
    constructor(page){
        this.page = page;
        this.leaveApproveBtn = page.getByRole('link',{name:'Approve'});
    }

    async goToLeaveApprove(){
        const isVisible = await this.leaveApproveBtn.first().isVisible({ timeout: 5000 }).catch(() => false);
        if (isVisible) {
            await this.leaveApproveBtn.first().click();
        } else {
            console.log('[leaveApprovals] No pending leave requests to approve — skipping.');
        }
        return isVisible;
    }
}
module.exports = LeaveApprovalsPage
