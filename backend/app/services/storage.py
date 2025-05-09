import faiss
import numpy as np
import sqlite3
import pickle

def get_dims():
    from app.services.embedding import model
    d = model.get_sentence_embedding_dimension()
    return d

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
# doc_id is the hash of the doc, db_id is the db it belongs to ... id, name is name of doc,  and embedding_bytes is the whole embedding of the doc, faiss index is the index of the 
# of the doc with text
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
  
    nembedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
    
    cur.execute("""
        INSERT INTO document_metadata (doc_id, db_id, name, embedding_bytes) 
        VALUES(?, ?, ?, ?)
    
    """, (doc_id, db_id, doc_name, sqlite3.Binary(nembedding.tobytes())))

    conn.commit()

    # creating a seperate index for sentence embeddings
    sent_index = faiss.IndexFlatL2(get_dims())

    # Add sentence embeddings to the Faiss index
    for emb in sentence_embeddings:
        emb_np = np.array(emb, dtype=np.float32).reshape(1, -1)
        sent_index.add(emb_np)

    # serialize the sentence embeddings 
    try: 
        faiss_index_serialized = pickle.dumps(sent_index) if sent_index.ntotal > 0 else None
    except:
        return "Error in converting faiss index"

    cur.execute("UPDATE document_metadata SET faiss_index=? WHERE doc_id=?", (sqlite3.Binary(faiss_index_serialized), doc_id))
    conn.commit()
    
    print(f"Saved Doc_id: {doc_id}")
