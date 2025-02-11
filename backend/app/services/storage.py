import faiss
import numpy as np
import sqlite3

def get_dims():
    from app.services.embedding import model
    d = model.get_sentence_embedding_dimension()
    return d

index = faiss.IndexFlatL2(get_dims())

conn = sqlite3.connect("documents.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS document (id TEXT PRIMARY KEY, name TEXT)")

def save_embedding(doc_id, doc_name, embedding):
    cur.execute("INSERT INTO document (id, name) VALUES(?, ?)", (doc_id, doc_name))
    conn.commit()
    index.add(embedding)

def get_embedding(doc_id):
    if not isinstance(doc_id, str):
        raise ValueError(f"Expected doc_id to be a string. but got {type(doc_id)}")

    cur.execute("SELECT id FROM document WHERE id=?", (doc_id,))
    return cur.fetchone()