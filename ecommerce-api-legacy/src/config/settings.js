const settings = {
  port: parseInt(process.env.PORT, 10) || 3000,
  paymentGatewayKey:
    process.env.PAYMENT_GATEWAY_KEY || 'pk_test_change_me_in_production',
  smtpUser: process.env.SMTP_USER || 'no-reply@fullcycle.com.br',
};

module.exports = settings;
