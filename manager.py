from task import Task
from db import execute_psql
from datetime import datetime

"""
The application should support the following functionalities: 
1. Add a new task. 
2. List all tasks with optional filtering (e.g., by due date, priority, or status). 
3. Update task details. 
4. Mark task as completed. 
5. Delete a task. 
"""

class TaskManager:

    def add_task(self, task: Task):
        query = """
        INSERT INTO tasks (title, description, due_date, priority, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        params = (task.title, task.description, task.due_date, task.priority, task.status)
        task_id = execute_psql(query, params, return_id=True)
        print(f"Task ID added: {task_id}")

    def list_tasks(self, filters=None):
        query = "SELECT * FROM tasks"
        conditions = []
        params = []

        if filters:
            if 'priority' in filters:
                conditions.append("priority = %s")
                params.append(filters['priority'])
            if 'due_date' in filters:
                conditions.append("due_date = %s")
                params.append(filters['due_date'])
            if 'status' in filters:
                conditions.append("status = %s")
                params.append(filters['status'])

        if conditions:  # Adds a WHERE clause
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC"

        rows = execute_psql(query, tuple(params), fetch_results=True)
        if not rows:
            print("No task records.")
            return

        for row in rows:
            task = Task(
                title=row[1],
                description=row[2],
                due_date=row[3],
                priority=row[4],
                status=row[5],
                created_at=row[6],
                task_id=row[0]
            )
            print(task)

        
    def update_task(self, task_id, updates: dict):
        if not updates:
            print("No updates.")
            return
        
        set_col = ', '.join(f"{k} = %s" for k in updates) # Generator expression for SET
        values = list(updates.values()) + [task_id]
        query = f"UPDATE tasks SET {set_col} WHERE id = %s;"
        execute_psql(query, tuple(values))
        print(f"Updated Task: {task_id}")

    def mark_task(self, task_id):
        query = "UPDATE tasks SET STATUS = 'Completed' WHERE id = %s;"
        execute_psql(query, (task_id,))
        print(f"Marked task {task_id} as completed.")

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = %s;"
        execute_psql(query, (task_id,))
        print(f"Task {task_id} deleted.")