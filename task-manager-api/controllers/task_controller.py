from sqlalchemy.orm import joinedload

from database import db
from models.category import Category
from models.task import Task
from models.user import User
from utils.helpers import (
    MAX_TITLE_LENGTH,
    MIN_TITLE_LENGTH,
    VALID_STATUSES,
    count_overdue_tasks,
    parse_date,
    task_list_item,
    utc_now,
)


class TaskController:
    @staticmethod
    def list_tasks():
        tasks = Task.query.options(
            joinedload(Task.user),
            joinedload(Task.category),
        ).all()
        return [task_list_item(t) for t in tasks], 200

    @staticmethod
    def get_task(task_id):
        task = db.session.get(Task, task_id)
        if not task:
            return {"error": "Task não encontrada"}, 404

        data = task.to_dict()
        data["overdue"] = task.is_overdue()
        return data, 200

    @staticmethod
    def create_task(data):
        if not data:
            return {"error": "Dados inválidos"}, 400

        title = data.get("title")
        if not title:
            return {"error": "Título é obrigatório"}, 400
        if len(title) < MIN_TITLE_LENGTH:
            return {"error": "Título muito curto"}, 400
        if len(title) > MAX_TITLE_LENGTH:
            return {"error": "Título muito longo"}, 400

        status = data.get("status", "pending")
        priority = data.get("priority", 3)
        user_id = data.get("user_id")
        category_id = data.get("category_id")
        due_date = data.get("due_date")
        tags = data.get("tags")

        if status not in VALID_STATUSES:
            return {"error": "Status inválido"}, 400
        if priority < 1 or priority > 5:
            return {"error": "Prioridade deve ser entre 1 e 5"}, 400

        if user_id and not db.session.get(User, user_id):
            return {"error": "Usuário não encontrado"}, 404
        if category_id and not db.session.get(Category, category_id):
            return {"error": "Categoria não encontrada"}, 404

        task = Task(
            title=title,
            description=data.get("description", ""),
            status=status,
            priority=priority,
            user_id=user_id,
            category_id=category_id,
        )

        if due_date:
            parsed = parse_date(due_date) if isinstance(due_date, str) else due_date
            if not parsed:
                return {"error": "Formato de data inválido. Use YYYY-MM-DD"}, 400
            task.due_date = parsed

        if tags:
            task.tags = ",".join(tags) if isinstance(tags, list) else tags

        try:
            db.session.add(task)
            db.session.commit()
            return task.to_dict(), 201
        except Exception:
            db.session.rollback()
            return {"error": "Erro ao criar task"}, 500

    @staticmethod
    def update_task(task_id, data):
        task = db.session.get(Task, task_id)
        if not task:
            return {"error": "Task não encontrada"}, 404
        if not data:
            return {"error": "Dados inválidos"}, 400

        if "title" in data:
            if len(data["title"]) < MIN_TITLE_LENGTH:
                return {"error": "Título muito curto"}, 400
            if len(data["title"]) > MAX_TITLE_LENGTH:
                return {"error": "Título muito longo"}, 400
            task.title = data["title"]

        if "description" in data:
            task.description = data["description"]

        if "status" in data:
            if data["status"] not in VALID_STATUSES:
                return {"error": "Status inválido"}, 400
            task.status = data["status"]

        if "priority" in data:
            if data["priority"] < 1 or data["priority"] > 5:
                return {"error": "Prioridade deve ser entre 1 e 5"}, 400
            task.priority = data["priority"]

        if "user_id" in data:
            if data["user_id"] and not db.session.get(User, data["user_id"]):
                return {"error": "Usuário não encontrado"}, 404
            task.user_id = data["user_id"]

        if "category_id" in data:
            if data["category_id"] and not db.session.get(Category, data["category_id"]):
                return {"error": "Categoria não encontrada"}, 404
            task.category_id = data["category_id"]

        if "due_date" in data:
            if data["due_date"]:
                parsed = parse_date(data["due_date"])
                if not parsed:
                    return {"error": "Formato de data inválido"}, 400
                task.due_date = parsed
            else:
                task.due_date = None

        if "tags" in data:
            tags = data["tags"]
            task.tags = ",".join(tags) if isinstance(tags, list) else tags

        task.updated_at = utc_now()

        try:
            db.session.commit()
            return task.to_dict(), 200
        except Exception:
            db.session.rollback()
            return {"error": "Erro ao atualizar"}, 500

    @staticmethod
    def delete_task(task_id):
        task = db.session.get(Task, task_id)
        if not task:
            return {"error": "Task não encontrada"}, 404

        try:
            db.session.delete(task)
            db.session.commit()
            return {"message": "Task deletada com sucesso"}, 200
        except Exception:
            db.session.rollback()
            return {"error": "Erro ao deletar"}, 500

    @staticmethod
    def search_tasks(query, status, priority, user_id):
        tasks = Task.query

        if query:
            tasks = tasks.filter(
                db.or_(
                    Task.title.like(f"%{query}%"),
                    Task.description.like(f"%{query}%"),
                )
            )

        if status:
            tasks = tasks.filter(Task.status == status)

        if priority:
            tasks = tasks.filter(Task.priority == int(priority))

        if user_id:
            tasks = tasks.filter(Task.user_id == int(user_id))

        return [t.to_dict() for t in tasks.all()], 200

    @staticmethod
    def task_stats():
        total = Task.query.count()
        pending = Task.query.filter_by(status="pending").count()
        in_progress = Task.query.filter_by(status="in_progress").count()
        done = Task.query.filter_by(status="done").count()
        cancelled = Task.query.filter_by(status="cancelled").count()
        overdue_count = count_overdue_tasks(Task.query.all())

        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "done": done,
            "cancelled": cancelled,
            "overdue": overdue_count,
            "completion_rate": round((done / total) * 100, 2) if total > 0 else 0,
        }, 200
