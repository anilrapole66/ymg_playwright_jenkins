class EmployeePage {
  constructor(page) {
    this.page = page;

    this.addEmployeeBtn = page.getByRole('link', { name: 'Add New Employee(s)' });

    this.uploadExcelBtn = page.getByRole('link', { name: 'Upload via Excel' });

    this.configurablesBtn = page.getByRole('link', {name: 'Configurables'});

    this.publicHolidayMenu = page.getByRole('link', { name: 'Public Holidays' });

    this.addPublicholiday = page.getByRole('link', {name:'+ Add Holiday'});

    this.leaveApprovalsBtn = page.getByRole('link', {name:'Leave Approvals'});

    this.assests = page.getByRole('link', {name: 'Assets'});

    this.manageInventory = page.getByRole('link',{name: 'Manage Inventory'});

    this.addInventory = page.getByRole('link',{name:'+ Add Inventory'});


    this.id = page.getByRole('textbox', { name: 'Employee ID' });
    this.name = page.getByRole('textbox', { name: 'Full Name' });
    this.email = page.getByRole('textbox', { name: 'Email' });
    this.dob = page.locator('#date_of_birth');
    this.phone = page.getByRole('textbox', { name: 'Phone' });
    this.customer = page.getByRole('combobox', { name: 'Customer' });
    this.designation = page.getByRole('textbox', { name: 'Designation' });
    this.dateOfJoining = page.locator('#date_of_joining');
    this.sowStartDate = page.locator('#sow_start_date');
    this.sowEndDate = page.locator('#sow_end_date');

    this.otAllowed = page.locator('#ot_allowed');
    this.phAllowed = page.locator('#ph_allowed');

    this.selectCountry = page.getByRole('combobox', { name: 'Select Country' });

    this.submitBtn = page.getByRole('button', { name: 'Add Employee' });
  }


  async openAddEmployeeForm() {
    await this.addEmployeeBtn.click();
  }

    async openConfigurables() {
    await this.configurablesBtn.click();
    // await this.page.waitForURL(/configurables/);
  }

  async goToPublicHoliday() {
    await this.publicHolidayMenu.click();
  }

  async AddPublicholiday(){
    await this.addPublicholiday.click();
    await this.page.waitForURL('/public-holidays/add/')
    }

    async goToLeaveApprovals(){
      await this.leaveApprovalsBtn.click();
    }

    async goToAssests(){
      await this.assests.click();
      // await this.page.waitForURL('');
    }

    async goToManageInventory(){
      await this.manageInventory.click();
      await this.page.waitForURL('/assets/inventory/');
    }

  async goToUploadEmployees() {
  await this.uploadExcelBtn.click();
  } 
  async goToAddInventory(){
    await this.addInventory.click();
  }

async deleteEmployee(empId) {

  await this.page.goto('/employee_list/');

  // wait table ready
  await this.page.locator('table').waitFor();

  // 🔎 search employee
  const searchBox = this.page.getByPlaceholder(/search/i);
  if (await searchBox.isVisible()) {
    await searchBox.fill(empId);
    await this.page.keyboard.press('Enter');
  }

  // wait results load
  await this.page.waitForTimeout(1000);

  const row = this.page.locator(`tr:has-text("${empId}")`);

  if (await row.count() === 0) {
    console.log(`⚠ Employee ${empId} not found for cleanup`);
    return;
  }

  await row.getByRole('button', { name: /delete/i }).click();
  await this.page.getByRole('button', { name: /confirm/i }).click();

  console.log(`🧹 Deleted employee ${empId}`);
}


    async addEmployee(data) {

    await this.id.fill(data.id);
    await this.name.fill(data.name);
    await this.email.fill(data.email);

    await this.dob.fill(data.dob);
    await this.phone.fill(data.phone);

    await this.customer.selectOption({ label: data.customer });
    await this.designation.fill(data.designation);
    

    await this.dateOfJoining.fill(data.dateOfJoining);
    await this.sowStartDate.fill(data.sowStartDate);
    await this.sowEndDate.fill(data.sowEndDate);

    // toggle handling
    if (data.otAllowed)
      await this.otAllowed.check();
    else
      await this.otAllowed.uncheck();

    if (data.phAllowed)
      await this.phAllowed.check();
    else
      await this.phAllowed.uncheck();

    await this.selectCountry.selectOption({ label: data.country });
    await Promise.all([
  this.page.waitForURL(/employee_list/),
  this.submitBtn.click()
]);

  }
}



module.exports = EmployeePage;

