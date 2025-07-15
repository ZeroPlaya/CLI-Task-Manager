from manager import TaskManager
from datetime import datetime
from task import Task


manager = TaskManager()

def setup_menu():
    print("\nTask actions:")
    print("1. List Tasks")
    print("2. List Tasks w/ Filter")
    print("3. Add Task")
    print("4. Update Task")
    print("5. Mark Task as completed")
    print("6. Delete Task")
    print("7. Exit Menu")

def cli_input():
    while True:
        setup_menu()
        user_input = input("Choose an action (1-7): ").strip()

        if user_input == "1":  # List Tasks
            manager.list_tasks()

        elif user_input == "2":  # List Tasks w/ Filter
            filters = {}
            priority = input("Priority (Low/Medium/High or blank): ").strip()
            status = input("Status (Pending/In Progress/Completed or blank): ").strip()
            due = input("Due Date (YYYY-MM-DD or blank): ").strip()

            if priority:
                filters['priority'] = priority
            if status:
                filters['status'] = status
            if due:
                try:
                    filters['due_date'] = datetime.strptime(due, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date filter. Ignoring due date filter.")

            manager.list_tasks(filters)

        elif user_input == "3":  # Add Task
            title = input("Title: ").strip()
            description = input("Description (optional): ").strip()
            due = input("Due Date (YYYY-MM-DD) or blank: ").strip()
            priority = input("Priority (Low/Medium/High) or blank [Medium]: ").strip() or "Medium"
            status = "Pending"

            due_date = None
            if due:
                try:
                    due_date = datetime.strptime(due, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format (YYYY-MM-DD). Due date will be empty.")

            task = Task(title=title, description=description, due_date=due_date, priority=priority, status=status)
            manager.add_task(task)

        elif user_input == "4":  # Update Task
            try:
                task_id = int(input("Task ID to update: ").strip())
                updates = {}
                print("Leave empty to skip updating a field.")
                title = input("New Title: ").strip()
                description = input("New Description: ").strip()
                due = input("New Due Date (YYYY-MM-DD): ").strip()
                priority = input("New Priority (Low/Medium/High): ").strip()
                status = input("New Status (Pending/In Progress/Completed): ").strip()

                if title:
                    updates['title'] = title
                if description:
                    updates['description'] = description
                if due:
                    try:
                        updates['due_date'] = datetime.strptime(due, "%Y-%m-%d").date()
                    except ValueError:
                        print("Invalid date format. Skipping due date update.")
                if priority:
                    updates['priority'] = priority
                if status:
                    updates['status'] = status

                manager.update_task_details(task_id, updates)
            except ValueError:
                print("Invalid Task ID.")

        elif user_input == "5":  # Mark Task as Completed
            try:
                task_id = int(input("Task ID to mark as completed: ").strip())
                manager.mark_task_completed(task_id)
            except ValueError:
                print("Invalid Task ID.")

        elif user_input == "6":  # Delete Task
            try:
                task_id = int(input("Task ID to delete: ").strip())
                manager.delete_task(task_id)
            except ValueError:
                print("Invalid Task ID.")

        elif user_input == "7":  # Exit Menu
            print("Exiting... Goodbye!")
            break

        else:
            print("Enter a valid number between 1 and 7.")