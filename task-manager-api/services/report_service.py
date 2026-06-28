from datetime import datetime, timedelta
from database import db
from models.task import Task
from models.user import User
from models.category import Category
from utils.helpers import format_date, calculate_percentage


class ReportService:
    def summary(self):
        total_tasks = Task.query.count()
        total_users = User.query.count()
        total_categories = Category.query.count()
        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()
        p1 = Task.query.filter_by(priority=1).count()
        p2 = Task.query.filter_by(priority=2).count()
        p3 = Task.query.filter_by(priority=3).count()
        p4 = Task.query.filter_by(priority=4).count()
        p5 = Task.query.filter_by(priority=5).count()

        overdue_count = 0
        overdue_list = []
        for task in Task.query.all():
            if task.due_date and task.due_date < datetime.utcnow() and task.status not in ['done', 'cancelled']:
                overdue_count += 1
                overdue_list.append({
                    'id': task.id,
                    'title': task.title,
                    'due_date': str(task.due_date),
                    'days_overdue': (datetime.utcnow() - task.due_date).days,
                })

        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_tasks = Task.query.filter(Task.created_at >= seven_days_ago).count()
        recent_done = Task.query.filter(Task.status == 'done', Task.updated_at >= seven_days_ago).count()

        user_stats = []
        for user in User.query.all():
            user_tasks = Task.query.filter_by(user_id=user.id).all()
            completed = sum(1 for task in user_tasks if task.status == 'done')
            total = len(user_tasks)
            user_stats.append({
                'user_id': user.id,
                'user_name': user.name,
                'total_tasks': total,
                'completed_tasks': completed,
                'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0,
            })

        return {
            'generated_at': str(datetime.utcnow()),
            'overview': {'total_tasks': total_tasks, 'total_users': total_users, 'total_categories': total_categories},
            'tasks_by_status': {'pending': pending, 'in_progress': in_progress, 'done': done, 'cancelled': cancelled},
            'tasks_by_priority': {'critical': p1, 'high': p2, 'medium': p3, 'low': p4, 'minimal': p5},
            'overdue': {'count': overdue_count, 'tasks': overdue_list},
            'recent_activity': {'tasks_created_last_7_days': recent_tasks, 'tasks_completed_last_7_days': recent_done},
            'user_productivity': user_stats,
        }

    def user_report(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        tasks = Task.query.filter_by(user_id=user_id).all()
        total = len(tasks)
        done = sum(1 for task in tasks if task.status == 'done')
        pending = sum(1 for task in tasks if task.status == 'pending')
        in_progress = sum(1 for task in tasks if task.status == 'in_progress')
        cancelled = sum(1 for task in tasks if task.status == 'cancelled')
        overdue = sum(1 for task in tasks if task.due_date and task.due_date < datetime.utcnow() and task.status not in ['done', 'cancelled'])
        high_priority = sum(1 for task in tasks if task.priority <= 2)
        return {
            'user': {'id': user.id, 'name': user.name, 'email': user.email},
            'statistics': {
                'total_tasks': total,
                'done': done,
                'pending': pending,
                'in_progress': in_progress,
                'cancelled': cancelled,
                'overdue': overdue,
                'high_priority': high_priority,
                'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
            },
        }

    def categories(self):
        result = []
        for category in Category.query.all():
            cat_data = category.to_dict()
            cat_data['task_count'] = Task.query.filter_by(category_id=category.id).count()
            result.append(cat_data)
        return result

    def create_category(self):
        from flask import request
        data = request.get_json() or {}
        name = data.get('name')
        if not name:
            raise ValueError('Nome é obrigatório')
        category = Category()
        category.name = name
        category.description = data.get('description', '')
        category.color = data.get('color', '#000000')
        db.session.add(category)
        db.session.commit()
        return category.to_dict()

    def update_category(self, cat_id):
        from flask import request
        category = Category.query.get(cat_id)
        if not category:
            raise LookupError('Categoria não encontrada')
        data = request.get_json() or {}
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        if 'color' in data:
            category.color = data['color']
        db.session.commit()
        return category.to_dict()

    def delete_category(self, cat_id):
        category = Category.query.get(cat_id)
        if not category:
            raise LookupError('Categoria não encontrada')
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Categoria deletada'}
