const CheckoutService = require('../services/checkoutService');

class CheckoutController {
  constructor(db) {
    this.checkoutService = new CheckoutService(db);
  }

  checkout(req, res) {
    const { usr: userName, eml: email, pwd: password, c_id: courseId, card } = req.body;
    this.checkoutService.createCheckout({ userName, email, password, courseId, cardNumber: card })
      .then((result) => res.status(200).json(result))
      .catch((error) => {
        if (error.message === 'Bad Request') return res.status(400).send('Bad Request');
        if (error.message === 'Curso não encontrado') return res.status(404).send('Curso não encontrado');
        if (error.message === 'Pagamento recusado') return res.status(400).send('Pagamento recusado');
        return res.status(500).send(error.message || 'Erro interno');
      });
  }

  financialReport(req, res) {
    this.checkoutService.getFinancialReport()
      .then((report) => res.json(report))
      .catch(() => res.status(500).send('Erro DB'));
  }

  deleteUser(req, res) {
    const { id } = req.params;
    this.checkoutService.deleteUser(id)
      .then((result) => res.status(200).json(result))
      .catch((error) => {
        if (error.message === 'Usuário não encontrado') return res.status(404).send('Usuário não encontrado');
        return res.status(500).send(error.message || 'Erro ao remover usuário');
      });
  }

}

module.exports = CheckoutController;
