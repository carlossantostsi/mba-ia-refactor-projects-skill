from flask import jsonify, request
from services.task_service import TaskService


class TaskController:
    def __init__(self):
        self.service = TaskService()

    def get_tasks(self):
        try:
            return jsonify(self.service.get_all()), 200
        except Exception:
            return jsonify({'error': 'Erro interno'}), 500

    def get_task(self, task_id):
        try:
            task = self.service.get_by_id(task_id)
            if task:
                return jsonify(task), 200
            return jsonify({'error': 'Task não encontrada'}), 404
        except Exception:
            return jsonify({'error': 'Erro interno'}), 500

    def create_task(self):
        try:
            data = request.get_json() or {}
            return jsonify(self.service.create(data)), 201
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
        except LookupError as exc:
            return jsonify({'error': str(exc)}), 404
        except Exception:
            return jsonify({'error': 'Erro ao criar task'}), 500

    def update_task(self, task_id):
        try:
            data = request.get_json() or {}
            return jsonify(self.service.update(task_id, data)), 200
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
        except LookupError as exc:
            return jsonify({'error': str(exc)}), 404
        except Exception:
            return jsonify({'error': 'Erro ao atualizar'}), 500

    def delete_task(self, task_id):
        try:
            self.service.delete(task_id)
            return jsonify({'message': 'Task deletada com sucesso'}), 200
        except LookupError as exc:
            return jsonify({'error': str(exc)}), 404
        except Exception:
            return jsonify({'error': 'Erro ao deletar'}), 500

    def search_tasks(self):
        query = request.args.get('q', '')
        status = request.args.get('status', '')
        priority = request.args.get('priority', '')
        user_id = request.args.get('user_id', '')
        return jsonify(self.service.search(query, status, priority, user_id)), 200

    def task_stats(self):
        return jsonify(self.service.stats()), 200


task_controller = TaskController()
