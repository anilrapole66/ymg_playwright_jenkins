const base = require('@playwright/test');

exports.test = base.test.extend({
  // you can add shared fixtures later here
});

exports.expect = base.expect;