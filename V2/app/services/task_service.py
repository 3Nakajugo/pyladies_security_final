from flask_jwt_extended import get_jwt_identity
from app.repositories import create_task as repo_create_task, get_tasks_by_user_id, get_task_by_id
from app.repositories.task_repository import update_task_status, delete_task
from app.repositories.user_repository import find_user_by_id
import uuid


def create_task_service(data):
    """Create a new task"""
    user_id = get_jwt_identity()
    
    # Convert string UUID to UUID object
    user_id_obj = uuid.UUID(user_id)
    
    title = data.get("title")
    description = data.get("description")
    assigned_to_id = data.get("assigned_to_id")
    
    if not title:
        return {"message": "Title is required"}, 400
    
    # Default assigned_to_id to creator_id if not provided
    if not assigned_to_id:
        assigned_to_id = user_id_obj
    else:
        # Verify assigned_to_id user exists if provided
        assigned_user = find_user_by_id(assigned_to_id)
        if not assigned_user:
            return {"message": "Assigned user not found"}, 404
    
    try:
        task = repo_create_task(
            title=title,
            description=description,
            created_by_id=user_id_obj,
            assigned_to_id=assigned_to_id
        )
        
        return {
            "message": "Task created successfully",
            "task": {
                "task_id": str(task.task_id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "created_by_id": str(task.created_by_id),
                "assigned_to_id": str(task.assigned_to_id) if task.assigned_to_id else None
            }
        }, 201
    except Exception as e:
        return {"message": f"Error creating task: {str(e)}"}, 500


def get_user_tasks_service():
    """Get all tasks for the authenticated user"""
    user_id = get_jwt_identity()
    user_id_obj = uuid.UUID(user_id)
    
    try:
        tasks = get_tasks_by_user_id(user_id_obj)
        
        tasks_list = [
            {
                "task_id": str(task.task_id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "created_by_id": str(task.created_by_id),
                "assigned_to_id": str(task.assigned_to_id) if task.assigned_to_id else None
            }
            for task in tasks
        ]
        
        return {
            "message": "Tasks retrieved successfully",
            "tasks": tasks_list,
            "count": len(tasks_list)
        }, 200
    except Exception as e:
        return {"message": f"Error retrieving tasks: {str(e)}"}, 500


def get_task_by_id_service(task_id):
    """Get a specific task by ID"""
    try:
        task = get_task_by_id(task_id)
        
        if not task:
            return {"message": "Task not found"}, 404
        
        return {
            "message": "Task retrieved successfully",
            "task": {
                "task_id": str(task.task_id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "created_by_id": str(task.created_by_id),
                "assigned_to_id": str(task.assigned_to_id) if task.assigned_to_id else None
            }
        }, 200
    except Exception as e:
        return {"message": f"Error retrieving task: {str(e)}"}, 500


def update_task_service(task_id, data):
    """Update a task"""
    user_id = get_jwt_identity()
    user_id_obj = uuid.UUID(user_id)
    
    try:
        task = get_task_by_id(task_id)
        
        if not task:
            return {"message": "Task not found"}, 404
        
        # Check if user is the creator or assigned user
        if task.created_by_id != user_id_obj and task.assigned_to_id != user_id_obj:
            return {"message": "You don't have permission to update this task"}, 403
        
        # Update task fields
        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "status" in data:
            task.status = data["status"]
        if "assigned_to_id" in data:
            if data["assigned_to_id"]:
                assigned_user = find_user_by_id(data["assigned_to_id"])
                if not assigned_user:
                    return {"message": "Assigned user not found"}, 404
            task.assigned_to_id = data["assigned_to_id"]
        
        update_task_status(task)
        
        return {
            "message": "Task updated successfully",
            "task": {
                "task_id": str(task.task_id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "created_by_id": str(task.created_by_id),
                "assigned_to_id": str(task.assigned_to_id) if task.assigned_to_id else None
            }
        }, 200
    except Exception as e:
        return {"message": f"Error updating task: {str(e)}"}, 500


def delete_task_service(task_id):
    """Delete a task"""
    user_id = get_jwt_identity()
    user_id_obj = uuid.UUID(user_id)
    
    try:
        task = get_task_by_id(task_id)
        
        if not task:
            return {"message": "Task not found"}, 404
        
        # Check if user is the creator
        if task.created_by_id != user_id_obj:
            return {"message": "Only the task creator can delete this task"}, 403
        
        delete_task(task_id)
        
        return {"message": "Task deleted successfully"}, 200
    except Exception as e:
        return {"message": f"Error deleting task: {str(e)}"}, 500
