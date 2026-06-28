const sqlite3 = require('sqlite3').verbose();
const { config } = require('./config');
const CheckoutController = require('./controllers/checkoutController');

class AppManager {
  constructor() {
    this.db = new sqlite3.Database(config.dbPath);
    this.checkoutController = new CheckoutController(this.db);
  }

  initDb() {
    this.db.serialize(() => {
      this.db.run('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, pass TEXT)');
      this.db.run('CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)');
      this.db.run('CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)');
      this.db.run('CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)');
      this.db.run('CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)');

      this.db.run("INSERT OR IGNORE INTO users (id, name, email, pass) VALUES (1, 'Leonan', 'leonan@fullcycle.com.br', '123')");
      this.db.run("INSERT OR IGNORE INTO courses (id, title, price, active) VALUES (1, 'Clean Architecture', 997.00, 1), (2, 'Docker', 497.00, 1)");
      this.db.run("INSERT OR IGNORE INTO enrollments (id, user_id, course_id) VALUES (1, 1, 1)");
      this.db.run("INSERT OR IGNORE INTO payments (id, enrollment_id, amount, status) VALUES (1, 1, 997.00, 'PAID')");
    });
  }

  setupRoutes(app) {
    app.post('/api/checkout', this.checkoutController.checkout.bind(this.checkoutController));
    app.get('/api/admin/financial-report', this.checkoutController.financialReport.bind(this.checkoutController));
    app.delete('/api/users/:id', this.checkoutController.deleteUser.bind(this.checkoutController));
  }
}

module.exports = AppManager;
