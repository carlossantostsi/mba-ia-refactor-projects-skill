const sqlite3 = require('sqlite3').verbose();
const { config } = require('../config');
const { logAndCache, hashPassword } = require('../utils');

class CheckoutService {
  constructor(db) {
    this.db = db;
  }

  async createCheckout({ userName, email, password, courseId, cardNumber }) {
    if (!userName || !email || !courseId || !cardNumber) {
      throw new Error('Bad Request');
    }

    return new Promise((resolve, reject) => {
      this.db.get('SELECT * FROM courses WHERE id = ? AND active = 1', [courseId], (err, course) => {
        if (err || !course) return reject(new Error('Curso não encontrado'));

        this.db.get('SELECT id FROM users WHERE email = ?', [email], (err, user) => {
          if (err) return reject(new Error('Erro DB'));

          const processPaymentAndEnroll = (userId) => {
            const status = cardNumber.startsWith('4') ? 'PAID' : 'DENIED';
            if (status === 'DENIED') return reject(new Error('Pagamento recusado'));

            this.db.run('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId], function (insertErr) {
              if (insertErr) return reject(new Error('Erro Matrícula'));
              const enrollmentId = this.lastID;
              this.db.run('INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)', [enrollmentId, course.price, status], function (paymentErr) {
                if (paymentErr) return reject(new Error('Erro Pagamento'));
                this.db.run('INSERT INTO audit_logs (action, created_at) VALUES (?, datetime(\'now\'))', [`Checkout curso ${courseId} por ${userId}`], (auditErr) => {
                  if (auditErr) return reject(new Error('Erro auditoria'));
                  logAndCache(`last_checkout_${userId}`, course.title);
                  resolve({ msg: 'Sucesso', enrollment_id: enrollmentId });
                });
              }.bind(this));
            }.bind(this));
          };

          if (!user) {
            const hash = hashPassword(password || '123456');
            this.db.run('INSERT INTO users (name, email, pass) VALUES (?, ?, ?)', [userName, email, hash], function (insertErr) {
              if (insertErr) return reject(new Error('Erro ao criar usuário'));
              processPaymentAndEnroll(this.lastID);
            }.bind(this));
          } else {
            processPaymentAndEnroll(user.id);
          }
        });
      });
    });
  }

  async getFinancialReport() {
    return new Promise((resolve, reject) => {
      this.db.all('SELECT * FROM courses', [], (err, courses) => {
        if (err) return reject(new Error('Erro DB'));
        const report = [];
        let pendingCourses = courses.length;
        if (pendingCourses === 0) return resolve(report);

        courses.forEach((course) => {
          const courseData = { course: course.title, revenue: 0, students: [] };
          this.db.all('SELECT * FROM enrollments WHERE course_id = ?', [course.id], (err, enrollments) => {
            let pendingEnrollments = enrollments.length;
            if (pendingEnrollments === 0) {
              report.push(courseData);
              pendingCourses -= 1;
              if (pendingCourses === 0) resolve(report);
              return;
            }

            enrollments.forEach((enrollment) => {
              this.db.get('SELECT name, email FROM users WHERE id = ?', [enrollment.user_id], (err, user) => {
                this.db.get('SELECT amount, status FROM payments WHERE enrollment_id = ?', [enrollment.id], (err, payment) => {
                  if (payment && payment.status === 'PAID') {
                    courseData.revenue += payment.amount;
                  }
                  courseData.students.push({
                    student: user ? user.name : 'Unknown',
                    paid: payment ? payment.amount : 0
                  });
                  pendingEnrollments -= 1;
                  if (pendingEnrollments === 0) {
                    report.push(courseData);
                    pendingCourses -= 1;
                    if (pendingCourses === 0) resolve(report);
                  }
                });
              });
            });
          });
        });
      });
    });
  }

  async deleteUser(userId) {

    return new Promise((resolve, reject) => {
      this.db.get('SELECT id FROM users WHERE id = ?', [userId], (err, user) => {
        if (err) return reject(new Error('Erro DB'));
        if (!user) return reject(new Error('Usuário não encontrado'));

        this.db.run(
          'DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id = ?)',
          [userId],
          (err) => {
            if (err) return reject(new Error('Erro ao deletar pagamentos'));
            this.db.run('DELETE FROM enrollments WHERE user_id = ?', [userId], (err) => {
              if (err) return reject(new Error('Erro ao deletar matrículas'));
              this.db.run('DELETE FROM users WHERE id = ?', [userId], (err) => {
                if (err) return reject(new Error('Erro ao deletar usuário'));
                resolve({ msg: 'Usuário e dados vinculados removidos com sucesso' });
              });
            });
          }
        );
      });
    });
  }
}


module.exports = CheckoutService;
