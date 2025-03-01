import faiss
import numpy as np
import sqlite3

# dict with keys => doc id and values => faiss index number; usef for retreiving the index based on doc id
doc_id_mapping = {}

# dict with keys => 
sentence_id_mapping = {}


def get_dims():
    from app.services.embedding import model
    d = model.get_sentence_embedding_dimension()
    return d

doc_index = faiss.IndexFlatL2(get_dims())
sent_index = faiss.IndexFlatL2(get_dims())

conn = sqlite3.connect("documents.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS document") ##for testing purposes ; clears data ; delete once deployed
conn.commit()

cur.execute("""
            CREATE TABLE IF NOT EXISTS document (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT KEY, 
            name TEXT, 
            embedding_bytes BLOB,
            sentence TEXT,
            sentence_embedding BLOB
            )
            """)

def save_embedding(doc_id, doc_name, embedding, text, sentence_embeddings):
    global doc_id_mapping
    
    nembedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
    print(nembedding.shape)
    cur.execute("INSERT INTO document (id, name, embedding_bytes) VALUES(?, ?, ?)", (doc_id, doc_name, sqlite3.Binary(embedding.tobytes())))
    conn.commit()
    doc_index.add(nembedding)
    faiss_index = doc_index.ntotal - 1
    doc_id_mapping[doc_id] = faiss_index

    for sent, emb in zip(text, sentence_embeddings):
        emb_np = np.array(emb, dtype=np.float32)
        cur.execute("INSERT INTO document (id, sentence, sentence_embedding) VALUES (?, ?, ?)", (doc_id, sent, sqlite3.Binary(emb_np.tobytes())))
        sent_index.add(emb_np.reshape(1, -1))
        sentence_id_mapping[sent_index.ntotal - 1] = doc_id
    conn.commit()
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
    cur.execute("SELECT sentence FROM document WHERE id=?", (doc_id,))
    result = cur.fetchone()
    if result:
        return result[0]
    return None
