import sqlite3

def get_db_connection():
    conn = sqlite3.connect("documents.db", timeout=30)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

