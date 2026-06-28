from datetime import datetime
from database import db
from models.task import Task
from models.user import User
from models.category import Category


class TaskService:
    def get_all(self):
        tasks = Task.query.all()
        return [self._serialize_task(t) for t in tasks]

    def get_by_id(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return None
        return self._serialize_task(task)

    def create(self, data):
        title = data.get('title')
        if not title:
            raise ValueError('Título é obrigatório')
        if len(title) < 3:
            raise ValueError('Título muito curto')
        if len(title) > 200:
            raise ValueError('Título muito longo')

        description = data.get('description', '')
        status = data.get('status', 'pending')
        priority = data.get('priority', 3)
        user_id = data.get('user_id')
        category_id = data.get('category_id')
        due_date = data.get('due_date')
        tags = data.get('tags')

        if status not in ['pending', 'in_progress', 'done', 'cancelled']:
            raise ValueError('Status inválido')
        if priority < 1 or priority > 5:
            raise ValueError('Prioridade deve ser entre 1 e 5')
        if user_id and not User.query.get(user_id):
            raise LookupError('Usuário não encontrado')
        if category_id and not Category.query.get(category_id):
            raise LookupError('Categoria não encontrada')

        task = Task()
        task.title = title
        task.description = description
        task.status = status
        task.priority = priority
        task.user_id = user_id
        task.category_id = category_id
        task.tags = ','.join(tags) if isinstance(tags, list) else tags
        if due_date:
            try:
                task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError as exc:
                raise ValueError('Formato de data inválido. Use YYYY-MM-DD') from exc

        db.session.add(task)
        db.session.commit()
        return task.to_dict()

    def update(self, task_id, data):
        task = Task.query.get(task_id)
        if not task:
            raise LookupError('Task não encontrada')

        if 'title' in data:
            if len(data['title']) < 3:
                raise ValueError('Título muito curto')
            if len(data['title']) > 200:
                raise ValueError('Título muito longo')
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            if data['status'] not in ['pending', 'in_progress', 'done', 'cancelled']:
                raise ValueError('Status inválido')
            task.status = data['status']
        if 'priority' in data:
            if data['priority'] < 1 or data['priority'] > 5:
                raise ValueError('Prioridade deve ser entre 1 e 5')
            task.priority = data['priority']
        if 'user_id' in data:
            if data['user_id'] and not User.query.get(data['user_id']):
                raise LookupError('Usuário não encontrado')
            task.user_id = data['user_id']
        if 'category_id' in data:
            if data['category_id'] and not Category.query.get(data['category_id']):
                raise LookupError('Categoria não encontrada')
            task.category_id = data['category_id']
        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                except ValueError as exc:
                    raise ValueError('Formato de data inválido') from exc
            else:
                task.due_date = None
        if 'tags' in data:
            task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
        task.updated_at = datetime.utcnow()

        db.session.commit()
        return task.to_dict()

    def delete(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            raise LookupError('Task não encontrada')
        db.session.delete(task)
        db.session.commit()
        return True

    def search(self, query, status, priority, user_id):
        tasks = Task.query
        if query:
            tasks = tasks.filter(db.or_(Task.title.like(f'%{query}%'), Task.description.like(f'%{query}%')))
        if status:
            tasks = tasks.filter(Task.status == status)
        if priority:
            tasks = tasks.filter(Task.priority == int(priority))
        if user_id:
            tasks = tasks.filter(Task.user_id == int(user_id))
        return [t.to_dict() for t in tasks.all()]

    def stats(self):
        total = Task.query.count()
        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()
        overdue_count = 0
        for task in Task.query.all():
            if task.due_date and task.due_date < datetime.utcnow() and task.status not in ['done', 'cancelled']:
                overdue_count += 1
        return {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'cancelled': cancelled,
            'overdue': overdue_count,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
        }

    def _serialize_task(self, task):
        data = task.to_dict()
        data['overdue'] = task.is_overdue()
        data['user_name'] = task.user.name if task.user else None
        data['category_name'] = task.category.name if task.category else None
        return data
