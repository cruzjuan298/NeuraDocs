import faiss
import numpy as np
import sqlite3

doc_id_mapping = {}
doc_to_text = {}


def get_dims():
    from app.services.embedding import model
    d = model.get_sentence_embedding_dimension()
    return d

index = faiss.IndexFlatL2(get_dims())

conn = sqlite3.connect("documents.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS document") ##for testing purposes ; clears data
conn.commit()

cur.execute("""
            CREATE TABLE IF NOT EXISTS document (
            id TEXT PRIMARY KEY, 
            name TEXT, 
            embedding_bytes BLOB,
            text TEXT
            )
            """)

def save_embedding(doc_id, doc_name, embedding, text):
    global doc_id_mapping

    embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
    cur.execute("INSERT INTO document (id, name, embedding_bytes, text) VALUES(?, ?, ?, ?)", (doc_id, doc_name, embedding.tobytes(), text))
    conn.commit()

    index.add(embedding)

    faiss_index = index.ntotal - 1
    doc_id_mapping[doc_id] = faiss_index
    
    print(f"Saved Doc_id: {doc_id} -> FAISS index: {faiss_index}")

def get_embedding(doc_id):
    if not isinstance(doc_id, str):
        doc_id = str(doc_id)

    cur.execute("SELECT id, name, embedding_bytes FROM document WHERE id=?", (doc_id,))
    
    result = cur.fetchone()

    if result:
        ndoc_id, doc_name, embedding_bytes = result
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        return ndoc_id, doc_name, embedding
    else:
        return None

def get_document_text(doc_id):
    cur.execute("SELECT text FROM document WHERE id=?", (doc_id,))
    result = cur.fetchone()
    if result:
        return result[0]
    return None