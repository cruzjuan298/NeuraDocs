import faiss
import numpy as np
import sqlite3
import pickle

# dict with keys => doc id and values => faiss index number; usef for retreiving the index based on doc id
doc_id_mapping = {}

# dict with keys => 
sentence_id_mapping = {}


def get_dims():
    from app.services.embedding import model
    d = model.get_sentence_embedding_dimension()
    return d

doc_index = faiss.IndexFlatL2(get_dims())

conn = sqlite3.connect("documents.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS document") ##for testing purposes ; clears data ; delete once deployed
conn.commit()

cur.execute("""
            CREATE TABLE IF NOT EXISTS document (
            doc_id TEXT, 
            name TEXT, 
            embedding_bytes BLOB,
            faiss_index BLOB
            )
            """)

def save_embedding(doc_id, doc_name, embedding, text, sentence_embeddings):
    global doc_id_mapping, sentence_id_mapping
    
    nembedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
    cur.execute("INSERT INTO document (doc_id, name, embedding_bytes) VALUES(?, ?, ?)", (doc_id, doc_name, sqlite3.Binary(embedding.tobytes())))
    conn.commit()
    doc_index.add(nembedding)
    faiss_index = doc_index.ntotal - 1
    doc_id_mapping[doc_id] = faiss_index

    # creating a seperate index for sentence embeddings
    sent_index = faiss.IndexFlatL2(get_dims())

    # Add sentence embeddings to the Faiss index
    for sent, emb in zip(text, sentence_embeddings):
        emb_np = np.array(emb, dtype=np.float32)
        sent_index.add(emb_np.reshape(1, -1))

    ##adding sentene index to dic 
    sentence_id_mapping[doc_id] = sent_index

    # serialize the sentence embeddings 
    faiss_index_serialized = pickle.dumps(sent_index)

    cur.execute("UPDATE document SET faiss_index=? WHERE doc_id=?", (sqlite3.Binary(faiss_index_serialized), doc_id))
    conn.commit()
    print(f"Saved Doc_id: {doc_id} -> FAISS index: {faiss_index}")

