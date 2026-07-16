const crypto = require('crypto');

const config = {
    dbUser: process.env.DB_USER || "admin_master",
    dbPass: process.env.DB_PASS || "", 
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || "",
    smtpUser: process.env.SMTP_USER || "no-reply@fullcycle.com.br",
    port: parseInt(process.env.PORT, 10) || 3000
};

let globalCache = {};
let totalRevenue = 0;

function logAndCache(key, data) {
    console.log(`[LOG] Salvando no cache: ${key}`);
    globalCache[key] = data;
}

function hashPassword(pwd) {
    const salt = process.env.HASH_SALT || "super-secure-salt-key-987";
    return crypto.createHmac('sha256', salt).update(pwd).digest('hex');
}

module.exports = { config, logAndCache, hashPassword, globalCache, totalRevenue };

