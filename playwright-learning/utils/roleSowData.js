function generateRoleSow() {
  const unique = Date.now();

  return {
    name: `AUTO_CLIENT_${unique}`,
    description: `AUTO_DESCRITION_${unique}`,
    mainClient:'Robert'
  };
}

module.exports = { generateRoleSow };
