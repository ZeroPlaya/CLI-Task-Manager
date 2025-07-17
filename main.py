from data.db_engine import create_tasks_table
from cli.interface import cli_input


def main():
    create_tasks_table()  # Ensure tasks table exists
    cli_input()


if __name__ == "__main__":
    main()
1