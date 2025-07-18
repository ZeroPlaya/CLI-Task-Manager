from datetime import datetime
from core.task import Task
from core.manager import TaskManager

manager = TaskManager()


def handle_filter_tasks():  # List Tasks w/ Filter
    pass


def handle_add_task():  # Add Task
    title = input("Title: ").strip()
    description = input("Description (optional): ").strip()
    due = input("Due Date (YYYY-MM-DD) or blank: ").strip()
    priority = input("Priority (Low/Medium/High) or blank [Medium]: "
                     ).strip() or "Medium"
    status = "Pending"

    due_date = None
    if due:
        try:
            due_date = datetime.strptime(due, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format (YYYY-MM-DD).")

    task = Task(title=title, description=description,
                due_date=due_date, priority=priority, status=status)
    manager.add_task(task)


def handle_update_task():
    try:
        task_id = int(input("Task ID to update: ").strip())
        updates = {}
        print("Leave empty to skip updating a field.")
        title = input("New Title: ").strip()
        description = input("New Description: ").strip()
        due = input("New Due Date (YYYY-MM-DD): ").strip()
        priority = input("New Priority (Low/Medium/High): ").strip()
        status = input("New Status (Pending/WIP/Done): ").strip()

        if title:
            updates['title'] = title
        if description:
            updates['description'] = description
        if due:
            try:
                updates['due_date'] = (
                    datetime.strptime(due, "%Y-%m-%d").date()
                )
            except ValueError:
                print("Invalid date format. Skipping due date update.")
        if priority:
            updates['priority'] = priority
        if status:
            updates['status'] = status

        manager.update_task(task_id, updates)
    except ValueError:
        print("Invalid Task ID.")


def handle_mark_task():
    try:
        task_id = int(input("Task ID to mark as completed: ").strip())
        manager.mark_task(task_id)
    except ValueError:
        print("Invalid Task ID.")


def handle_delete_task():
    try:
        task_id = int(input("Task ID to delete: ").strip())
        manager.delete_task(task_id)
    except ValueError:
        print("Invalid Task ID.")
