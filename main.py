from manager import TaskManager
from task import Task
from datetime import datetime
from db_engine import create_tasks_table
from interface import cli_input


def main():
    create_tasks_table()  # Ensure tasks table exists
    cli_input()

if __name__ == "__main__":
    main()
