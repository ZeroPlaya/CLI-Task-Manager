import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

__all__ = ['execute_psql']

print("Loaded DB credentials:")
# print("DB_USER =", os.getenv("DB_USER"))
# print("DB_PASSWORD =", os.getenv("DB_PASSWORD"))


def execute_psql(query, params=None, fetch_results=False, return_id=False):
    results = None
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        cur.execute(query, params)
        if fetch_results:
            results = cur.fetchall()
        elif return_id:
            results = cur.fetchone()[0]  # Return the first column (id)
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Execution failed: {e}")
    finally:
        if conn:
            conn.close()
    return results