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

conn = sqlite3.connect("documents.db", timeout=30)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS document") ##for testing purposes ; clears data ; delete once deployed
conn.commit()

cur.execute("DROP TABLE IF EXISTS document_metadata")
conn.commit()

cur.execute("""
            CREATE TABLE IF NOT EXISTS document (
            db_id TEXT PRIMARY KEY,
            name TEXT
            )
            """)


# mapping table for db_id to multiple doc_id values
cur.execute("""
            CREATE TABLE IF NOT EXISTS document_metadata (
            doc_id TEXT PRIMARY KEY,
            db_id TEXT,
            name TEXT,
            embedding_bytes BLOB,
            faiss_index BLOB,
            FOREIGN KEY (db_id) REFERENCES document(db_id) on DELETE CASCADE
            )
""")

def insertDb(dbId, db_name):
    try:
        cur.execute("""
                    INSERT INTO document VALUES (?, ?)
                    """, (dbId, db_name))
        conn.commit()
        return "Inserted DB"
    except Exception as e:
        return e


def save_embedding(db_id, doc_id, doc_name, embedding, text, sentence_embeddings):
    global doc_id_mapping, sentence_id_mapping
    
    nembedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
    
    cur.execute("""
        INSERT INTO document_metadata (doc_id, db_id, name, embedding_bytes) 
        VALUES(?, ?, ?, ?)
    
    """, (doc_id, db_id, doc_name, sqlite3.Binary(nembedding.tobytes())))

    conn.commit()

    doc_index.add(nembedding)
    faiss_index = doc_index.ntotal - 1
    doc_id_mapping[doc_id] = faiss_index

    # creating a seperate index for sentence embeddings
    sent_index = faiss.IndexFlatL2(get_dims())

    # Add sentence embeddings to the Faiss index
    for emb in sentence_embeddings:
        emb_np = np.array(emb, dtype=np.float32).reshape(1, -1)
        sent_index.add(emb_np)

    ##adding sentene index to dic 
    sentence_id_mapping[doc_id] = sent_index

    # serialize the sentence embeddings 

    try: 
        faiss_index_serialized = pickle.dumps(sent_index) if sent_index.ntotal > 0 else None
    except:
        return "Error in converting faiss index"

    cur.execute("UPDATE document_metadata SET faiss_index=? WHERE doc_id=?", (sqlite3.Binary(faiss_index_serialized), doc_id))
    conn.commit()
    print(f"Saved Doc_id: {doc_id} -> FAISS index: {faiss_index}")
