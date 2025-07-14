from db import execute_psql


def create_tasks_table():
    query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(32) NOT NULL,
        description VARCHAR(255),
        due_date DATE,
        priority VARCHAR(10),
        status VARCHAR(32),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_psql(query)
