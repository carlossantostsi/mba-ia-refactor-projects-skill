from flask import jsonify, request
from services.user_service import UserService


class UserController:
    def __init__(self):
        self.service = UserService()

    def get_users(self):
        return jsonify(self.service.get_all()), 200

    def get_user(self, user_id):
        user = self.service.get_by_id(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        return jsonify(user), 200

    def create_user(self):
        try:
            data = request.get_json() or {}
            return jsonify(self.service.create(data)), 201
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
        except LookupError as exc:
            return jsonify({'error': str(exc)}), 409
        except Exception:
            return jsonify({'error': 'Erro ao criar usuário'}), 500

    def update_user(self, user_id):
        try:
            data = request.get_json() or {}
            return jsonify(self.service.update(user_id, data)), 200
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
        except LookupError as exc:
            return jsonify({'error': str(exc)}), 409
        except Exception:
            return jsonify({'error': 'Erro ao atualizar'}), 500

    def delete_user(self, user_id):
        try:
            self.service.delete(user_id)
            return jsonify({'message': 'Usuário deletado com sucesso'}), 200
        except LookupError as exc:
            return jsonify({'error': str(exc)}), 404
        except Exception:
            return jsonify({'error': 'Erro ao deletar'}), 500

    def get_user_tasks(self, user_id):
        user = self.service.get_by_id(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        return jsonify(self.service.get_tasks(user_id)), 200

    def login(self):
        try:
            data = request.get_json() or {}
            return jsonify(self.service.login(data)), 200
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
        except PermissionError as exc:
            return jsonify({'error': str(exc)}), 403
        except LookupError as exc:
            return jsonify({'error': str(exc)}), 401


user_controller = UserController()
