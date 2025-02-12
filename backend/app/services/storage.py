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

cur.execute("DROP TABLE IF EXISTS document")
conn.commit()

cur.execute("CREATE TABLE IF NOT EXISTS document (id TEXT PRIMARY KEY, name TEXT, embedding_bytes BLOB)")

def save_embedding(doc_id, doc_name, embedding):
    embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
    cur.execute("INSERT INTO document (id, name, embedding_bytes) VALUES(?, ?, ?)", (doc_id, doc_name, embedding.tobytes()))
    conn.commit()

    index.add(embedding)

def get_embedding(doc_id):
    if not isinstance(doc_id, str):
        raise ValueError(f"Expected doc_id to be a string. but got {type(doc_id)}")

    cur.execute("SELECT id, name, embedding_bytes FROM document WHERE id=?", (doc_id,))
    result = cur.fetchone()

    if result:
        ndoc_id, doc_name, embedding_bytes = result
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        return ndoc_id, doc_name, embedding
    else:
        return None