from flask import jsonify
from services.report_service import ReportService


class ReportController:
    def __init__(self):
        self.service = ReportService()

    def summary_report(self):
        return jsonify(self.service.summary()), 200

    def user_report(self, user_id):
        report = self.service.user_report(user_id)
        if report is None:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        return jsonify(report), 200

    def get_categories(self):
        return jsonify(self.service.categories()), 200

    def create_category(self):
        return jsonify(self.service.create_category()), 201

    def update_category(self, cat_id):
        return jsonify(self.service.update_category(cat_id)), 200

    def delete_category(self, cat_id):
        return jsonify(self.service.delete_category(cat_id)), 200


report_controller = ReportController()
