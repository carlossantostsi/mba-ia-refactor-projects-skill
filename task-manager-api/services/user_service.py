import re
from datetime import datetime
from database import db
from models.user import User
from models.task import Task


class UserService:
    def get_all(self):
        users = User.query.all()
        result = []
        for user in users:
            user_data = user.to_dict()
            user_data['task_count'] = len(user.tasks)
            result.append(user_data)
        return result

    def get_by_id(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        data = user.to_dict()
        tasks = Task.query.filter_by(user_id=user_id).all()
        data['tasks'] = [task.to_dict() for task in tasks]
        return data

    def create(self, data):
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not name:
            raise ValueError('Nome é obrigatório')
        if not email:
            raise ValueError('Email é obrigatório')
        if not password:
            raise ValueError('Senha é obrigatória')
        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
            raise ValueError('Email inválido')
        if len(password) < 4:
            raise ValueError('Senha deve ter no mínimo 4 caracteres')
        if role not in ['user', 'admin', 'manager']:
            raise ValueError('Role inválido')
        if User.query.filter_by(email=email).first():
            raise LookupError('Email já cadastrado')

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.role = role
        db.session.add(user)
        db.session.commit()
        return user.to_dict()

    def update(self, user_id, data):
        user = User.query.get(user_id)
        if not user:
            raise LookupError('Usuário não encontrado')
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', data['email']):
                raise ValueError('Email inválido')
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                raise LookupError('Email já cadastrado')
            user.email = data['email']
        if 'password' in data:
            if len(data['password']) < 4:
                raise ValueError('Senha muito curta')
            user.set_password(data['password'])
        if 'role' in data:
            if data['role'] not in ['user', 'admin', 'manager']:
                raise ValueError('Role inválido')
            user.role = data['role']
        if 'active' in data:
            user.active = data['active']
        db.session.commit()
        return user.to_dict()

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise LookupError('Usuário não encontrado')
        for task in Task.query.filter_by(user_id=user_id).all():
            db.session.delete(task)
        db.session.delete(user)
        db.session.commit()
        return True

    def get_tasks(self, user_id):
        tasks = Task.query.filter_by(user_id=user_id).all()
        result = []
        for task in tasks:
            task_data = {}
            task_data['id'] = task.id
            task_data['title'] = task.title
            task_data['description'] = task.description
            task_data['status'] = task.status
            task_data['priority'] = task.priority
            task_data['created_at'] = str(task.created_at)
            task_data['due_date'] = str(task.due_date) if task.due_date else None
            task_data['overdue'] = task.is_overdue()
            result.append(task_data)
        return result

    def login(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise ValueError('Email e senha são obrigatórios')
        user = User.query.filter_by(email=email).first()
        if not user:
            raise LookupError('Credenciais inválidas')
        if not user.check_password(password):
            raise LookupError('Credenciais inválidas')
        if not user.active:
            raise PermissionError('Usuário inativo')
        return {
            'message': 'Login realizado com sucesso',
            'user': user.to_dict(),
            'token': 'fake-jwt-token-' + str(user.id)
        }
