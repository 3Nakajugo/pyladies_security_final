from app.models import Task
from app.extensions import db


def create_task(title, description=None, created_by_id=None, assigned_to_id=None):
    try:
        task = Task(
            title=title,
            description=description,
            created_by_id=created_by_id,
            assigned_to_id=assigned_to_id
        )
        db.session.add(task)
        db.session.commit()
        return task
    except Exception as e:
        db.session.rollback()
        raise e


def get_all_tasks():
    return Task.query.all()

def get_task_by_id(task_id):
    return Task.query.get(task_id)

def get_tasks_by_user_id(user_id):
    return Task.query.filter((Task.created_by_id == user_id) | (Task.assigned_to_id == user_id)).all()


def update_task_status(task):
    """Update task in database"""
    try:
        db.session.commit()
        return task
    except Exception as e:
        db.session.rollback()
        raise e


def delete_task(task_id):
    """Delete a task by ID"""
    try:
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
        return task
    except Exception as e:
        db.session.rollback()
        raise e
