import sqlite3
from app.db.connection import get_db_connection

def create_db():
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

            cur.execute("DROP TABLE IF EXISTS document")
            cur.execute("DROP TABLE IF EXISTS document_metadata")

            cur.execute("""
                CREATE TABLE document (
                db_id TEXT PRIMARY KEY,
                name TEXT
                )
                """)
            
            # mapping table for db_id to multiple doc_id values
            # doc_id is the hash of the doc, db_id is the db it belongs to
            # name is name of doc
            # embedding_bytes is the whole embedding of the doc
            # faiss_index is the index of the doc with text
            # text_content is the list of sentences stored as JSON
            cur.execute("""
                CREATE TABLE document_metadata (
                doc_id TEXT PRIMARY KEY,
                db_id TEXT,
                name TEXT,
                embedding_bytes BLOB, 
                faiss_index_bytes BLOB,
                text_content TEXT,
                FOREIGN KEY (db_id) REFERENCES document(db_id) on DELETE CASCADE
                )
            """)

        return {"message" : "successfully created database table", "success" : True}
    except sqlite3.Error as e:
        print(f"There has been an error when creating the intial database tables, {str(e)}")

        if conn:
            conn.rollback()
        return {"error" : str(e), "message" : "Check error for more details", "success" : False}
       
