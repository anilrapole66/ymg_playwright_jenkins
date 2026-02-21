const {test, expect} = require('./baseTest');
const LoginPage = require('../pages/loginPage');
const EmployeePage = require('../pages/employeePage');
const AssestAddInventoryPage = require('../pages/assestsAddInventoryPage');
const users = require('../testData/users.json');

test ('Add Inventory Flow', async({page}) => {

    const login = new LoginPage(page);
    const emp = new EmployeePage(page);
    const assest = new AssestAddInventoryPage(page);


    await login.open();
    await login.login(users.admin.username, users.admin.password);
    await emp.goToAssests();
    await emp.goToManageInventory();
    await emp.goToAddInventory();
    
     
    await assest.addAssestInventory({
    assestType: 'laptop',
    assestColor: 'black',
    serialNumber: '123',
    purchasedAt: 'store',
    purchasedDate: '2026-01-26',
    lastRepairedOn: '2025-01-26',
    description: 'Automation Test Holiday',
    lastRepairDetails:'color change',
    isActive : true
    
  });
});
