import psycopg2
from dotenv import load_dotenv
import os

__all__ = ['execute_psql']


def connect_db():
    try:
        load_dotenv()
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        raise


def execute_psql(query, params=None, fetch_results=False, return_id=False):
    results = None
    conn = None
    try:
        with connect_db() as conn, conn.cursor() as cur:
            cur.execute(query, params)
            if fetch_results:
                results = cur.fetchall()
            elif return_id:
                results = cur.fetchone()[0]  # Return the first column (id)
            else:
                results = None
            conn.commit()  # Apply changes to db
            return results
    except Exception as e:
        print(f"Execution failed: {e}")
        return None
