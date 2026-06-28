const config = {
  port: process.env.PORT || 3000,
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || 'pk_live_1234567890abcdef',
  dbPath: process.env.DB_PATH || ':memory:'
};

module.exports = { config };
