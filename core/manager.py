from .task import Task
from data.db import execute_psql
# from datetime import datetime

"""
The application should support the following functionalities:
1. Add a new task.
2. List tasks with optional filtering (e.g., by due date, priority, or status).
3. Update task details.
4. Mark task as completed.
5. Delete a task.
"""


class TaskManager:
    def add_task(self, task: Task):
        params = (task.title,
                  task.description,
                  task.due_date,
                  task.priority,
                  task.status)
        query = """
        INSERT INTO tasks (title, description, due_date, priority, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """

        task_id = execute_psql(query, params, return_id=True)
        print(f"Task ID added: {task_id}")

    def list_tasks(self):
        query = "SELECT * FROM tasks ORDER BY created_at DESC"
        rows = execute_psql(query, fetch_results=True)

        if not rows:
            print("No task records.")
            return []

        print("")
        for row in rows:
            task = Task(
                task_id=row[0],
                title=row[1],
                description=row[2],
                due_date=row[3],
                priority=row[4],
                status=row[5],
                created_at=row[6]
            )
            print(task)

    def update_task(self, task_id, updates: dict):
        if not updates:
            print("No updates.")
            return

        """SET column = %s, ..."""
        col_name = [f"{column} = %s" for column in updates]
        set_col = ', '.join(col_name)

        query = f"UPDATE tasks SET {set_col} WHERE id = %s;"
        values = [*updates.values(), task_id]

        execute_psql(query, params=tuple(values))
        updated_col = ', '.join(updates.keys())
        print(f"Updated Task {task_id}: {updated_col}")

    def mark_task(self, task_id):
        query = "UPDATE tasks SET status = 'Completed' WHERE id = %s;"
        execute_psql(query, params=(task_id,))
        print(f"Marked task {task_id} as completed.")

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = %s;"
        execute_psql(query, params=(task_id,))
        print(f"Task {task_id} deleted.")
