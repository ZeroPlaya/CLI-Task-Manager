from datetime import datetime


class Task:
    def __init__(self,
                 title,
                 description="",
                 due_date=None,
                 priority="Medium",
                 status="Pending",
                 created_at=None,
                 task_id=None):

        self.id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.created_at = created_at or datetime.now()

    def __str__(self):
        return (
            f"{self.id}, {self.title}, {self.description}, {self.due_date}, "
            f"{self.priority}, {self.status}, {self.created_at}"
        )
