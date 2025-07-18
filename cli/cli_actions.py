from datetime import datetime
from core.task import Task
from core.manager import TaskManager
from data.db import execute_psql

manager = TaskManager()


def handle_filter_tasks():  # List Tasks w/ Filter
    pass


def handle_add_task():  # Add Task
    title = input("Title: ").strip()
    description = input("Description (optional): ").strip() or None
    due = input("Due Date (YYYY-MM-DD) or blank: ").strip()
    priority = input("Priority (Low/Medium/High): ").strip() or "Medium"
    if priority not in {"Low", "Medium", "High"}:
        print("Invalid priority. Defaulting to 'Medium'.")
    status = "Pending"

    due_date = parse_date(due)

    task = Task(title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status)
    manager.add_task(task)


def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format (YYYY-MM-DD).")
        return None


def validate_task_id(task_id):
    if not isinstance(task_id, int):
        print("Task ID must be an integer.")
        return None

    query = "SELECT 1 FROM tasks WHERE id = %s LIMIT 1;"
    result = execute_psql(query, params=(task_id,), fetch_results=True)

    if not result:
        print(f"Task ID {task_id} does not exist.")
        return None

    return task_id


def handle_update_task():
    try:
        raw_id = int(input("Task ID to update: ").strip())
    except ValueError:
        print("Task ID must be an integer.")
        return

    task_id = validate_task_id(raw_id)
    if task_id is None:
        return

    print("Leave empty to skip updating a field.\n")

    fields = {
        "title": input("Title: ").strip(),
        "description": input("Description: ").strip(),
        "due_date": input("Due Date (YYYY-MM-DD): ").strip(),
        "priority": input("Priority (Low/Medium/High): ").strip().capitalize(),
        "status": input("Status (Pending/WIP/Done): ").strip().capitalize()
    }

    """If value exists, store key:value in dict"""
    updates = {key: value for key, value in fields.items() if value}
    manager.update_task(raw_id, updates)


def handle_mark_task():
    try:
        task_id = int(input("Task ID to mark as completed: ").strip())
    except ValueError:
        print("Task ID must be an integer.")

    task_id = validate_task_id(task_id)
    if task_id is None:
        return

    manager.mark_task(task_id)
    print(f"Task ID {task_id} marked as completed.")


def handle_delete_task():
    try:
        task_id = int(input("Task ID to delete: ").strip())
    except ValueError:
        print("Task ID must be an integer.")

    task_id = validate_task_id(task_id)
    if task_id is None:
        return

    answer = input(f"Delete {task_id} (Y/N)? ").strip().capitalize()
    if answer == "Y":
        manager.delete_task(task_id)
        print(f"Task ID {task_id} deleted.")
    elif answer == "N":
        print("Task deletion canceled.")
    else:
        print("Invalid input (Y/N).")
