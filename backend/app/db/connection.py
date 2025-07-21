import os
import sqlite3
import contextlib
from dotenv import load_dotenv

load_dotenv()

database_path = os.getenv("DATABASE_PATH")

@contextlib.contextmanager
def get_db_connection():
    conn = sqlite3.connect(database_path, timeout=30)
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()

