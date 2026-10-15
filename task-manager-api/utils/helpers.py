from datetime import datetime, timezone
import re

VALID_STATUSES = ["pending", "in_progress", "done", "cancelled"]
VALID_ROLES = ["user", "admin", "manager"]
MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 3
MIN_PASSWORD_LENGTH = 4
DEFAULT_PRIORITY = 3
DEFAULT_COLOR = "#000000"


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def format_date(date_obj):
    if date_obj:
        return str(date_obj)
    return None


def calculate_percentage(part, total):
    if total == 0:
        return 0
    return round((part / total) * 100, 2)


def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", email))


def sanitize_string(s):
    if s:
        return s.strip()
    return s


def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_string, "%d/%m/%Y")
        except ValueError:
            return None


def is_valid_color(color):
    return bool(color and len(color) == 7 and color[0] == "#")


def count_overdue_tasks(tasks):
    return sum(1 for t in tasks if t.is_overdue())


def overdue_task_entry(task):
    now = utc_now()
    return {
        "id": task.id,
        "title": task.title,
        "due_date": str(task.due_date),
        "days_overdue": (now - task.due_date).days,
    }


def task_list_item(task):
    task_data = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "user_id": task.user_id,
        "category_id": task.category_id,
        "created_at": str(task.created_at),
        "updated_at": str(task.updated_at),
        "due_date": str(task.due_date) if task.due_date else None,
        "tags": task.tags.split(",") if task.tags else [],
        "overdue": task.is_overdue(),
        "user_name": task.user.name if task.user else None,
        "category_name": task.category.name if task.category else None,
    }
    return task_data


def user_task_summary_item(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "created_at": str(task.created_at),
        "due_date": str(task.due_date) if task.due_date else None,
        "overdue": task.is_overdue(),
    }
