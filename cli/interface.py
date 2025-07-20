from core.manager import TaskManager
from cli.cli_actions import (
    handle_filter_tasks,
    handle_add_task,
    handle_delete_task,
    handle_mark_task,
    handle_update_task
)


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
    manager = TaskManager()
    while True:
        setup_menu()
        user_input = input("Choose an action (1-7): ").strip()

        if user_input == "1":  # List Tasks
            manager.list_tasks()

        elif user_input == "2":  # List Tasks w/ Filter
            handle_filter_tasks()

        elif user_input == "3":  # Add Task
            handle_add_task()

        elif user_input == "4":  # Update Task
            handle_update_task()

        elif user_input == "5":  # Mark Task as Completed
            handle_mark_task()

        elif user_input == "6":  # Delete Task
            handle_delete_task()

        elif user_input == "7":  # Exit Menu
            print("Exiting... Goodbye!")
            break

        else:
            print("Enter a valid number between 1 and 7.")
