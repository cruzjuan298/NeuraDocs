import faiss
import numpy as np
import sqlite3
import pickle
import json

def get_dims():
    from app.services.embedding import model
    d = model.get_sentence_embedding_dimension()
    return d

conn = sqlite3.connect("documents.db", timeout=30)
cur = conn.cursor()

# Create tables if they don't exist
cur.execute("""
            CREATE TABLE IF NOT EXISTS document (
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
            CREATE TABLE IF NOT EXISTS document_metadata (
            doc_id TEXT PRIMARY KEY,
            db_id TEXT,
            name TEXT,
            embedding_bytes BLOB, 
            faiss_index BLOB,
            text_content TEXT,
            FOREIGN KEY (db_id) REFERENCES document(db_id) on DELETE CASCADE
            )
""")
conn.commit()

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
    try:
        if not sentence_embeddings or len(sentence_embeddings) == 0:
            return {"error": "No sentence embeddings provided for document"}
            
        nembedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
        
        # Convert text list to JSON string
        text_json = json.dumps(text)
        
        # Create a separate index for sentence embeddings
        sent_index = faiss.IndexFlatL2(get_dims())

        # Add sentence embeddings to the Faiss index
        for emb in sentence_embeddings:
            emb_np = np.array(emb, dtype=np.float32).reshape(1, -1)
            sent_index.add(emb_np)

        if sent_index.ntotal == 0:
            return {"error": "Failed to create sentence embeddings index"}

        # Serialize the sentence embeddings 
        try: 
            faiss_index_serialized = pickle.dumps(sent_index)
        except Exception as e:
            print(f"Error serializing FAISS index: {str(e)}")
            return {"error": "Error in converting faiss index"}

        # Insert document with all data
        cur.execute("""
            INSERT INTO document_metadata (doc_id, db_id, name, embedding_bytes, faiss_index, text_content) 
            VALUES(?, ?, ?, ?, ?, ?)
        """, (doc_id, db_id, doc_name, sqlite3.Binary(nembedding.tobytes()), 
              sqlite3.Binary(faiss_index_serialized), text_json))

        conn.commit()
        
        print(f"Saved Doc_id: {doc_id}")
        return {"message": "Document saved successfully", "doc_id": doc_id}
        
    except Exception as e:
        print(f"Error saving document: {str(e)}")
        return {"error": f"Failed to save document: {str(e)}"}
