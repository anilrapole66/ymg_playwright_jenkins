function generateClient() {
  const unique = Date.now();

  return {
    name: `AUTO_CLIENT_${unique}`,
  };
}

module.exports = { generateClient };
