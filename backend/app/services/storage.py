import faiss
import numpy as np
import sqlite3
import json
import os
from app.db.connection import get_db_connection

def get_dims():
    from app.services.embedding import model
    d = model.get_sentence_embedding_dimension()
    return d

def insertDb(dbId, db_name):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                        INSERT INTO document VALUES (?, ?)
                        """, (dbId, db_name))
            return "Database inserted successfully"
    except sqlite3.IntegrityError:
        return f"Error: Database with id {dbId} already exists"
    except Exception as e:
        return f"Error occurred: {str(e)}"

## there was an issue with using the built-in faiss serialization method. Its best to work around this by manually serializing it.
## Pipeline: write index info to a faiss file => read info into a variable => delete file => return variable with 
def serialize(index):
    faiss_index_bytes = None
    file_name = "document_sentence_index.faiss"

    try:
        faiss.write_index(index, file_name)
        
        with open(file_name, "rb") as f:
            faiss_index_bytes = f.read()

    except Exception as e:
        print(f"(Debug) Error in trying to delete file with the faiss serilzation information. Error: {str(e)}")
        return None
    
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
                
    return faiss_index_bytes

def save_embedding(db_id, doc_id, doc_name, embedding, text, sentence_embeddings):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            print(f"(Debug) Starting save_embedding for doc_id: {doc_id}")
            
            # checks sentence embeddings if its empty based on size or length attribute, accounting for wether sentence embedding is numpy array (second conditional); had previous error where it was ambiguous when trying to search sentence embedding as a numpy array
            if sentence_embeddings is None or (hasattr(sentence_embeddings, 'size') and sentence_embeddings.size == 0) or (hasattr(sentence_embeddings, '__len__') and len(sentence_embeddings) == 0):
                print(f"(Debug) No sentence embeddings provided")
                return {"error": "No sentence embeddings provided for document"}
            
            print(f"(Debug) Sentence embeddings shape: {getattr(sentence_embeddings, 'shape', 'N/A')}")
            nembedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
            print(f"(Debug) Document embedding shape: {nembedding.shape}")
            
            text_json = json.dumps(text)
            print(f"(Debug) Text content length: {len(text_json)}")

            try:
                dim = get_dims()
                print(f"(Debug) FAISS index dimension: {dim}")
            except Exception as e:
                print(f"(Debug) Failed to get FAISS dimension: {str(e)}")
                return {"error" : "Embedding model not avilable or failed to load"}
            
            sent_index = faiss.IndexFlatL2(dim)

            for i, emb in enumerate(sentence_embeddings):
                emb_np = np.array(emb, dtype=np.float32).reshape(1, -1)
                sent_index.add(emb_np)
            print(f"(Debug) Added {len(sentence_embeddings)} embeddings to FAISS index")

            if sent_index.ntotal == 0:
                print(f"(Debug) FAISS index is empty after adding embeddings")
                return {"error": "Failed to create sentence embeddings index"}

            faiss_index_bytes = serialize(sent_index)
            print(f"Type of faiss_index_bytes: {type(faiss_index_bytes)}")

            nembedding_bytes = nembedding.tobytes()

            try:
                cur.execute("""
                    INSERT INTO document_metadata (doc_id, db_id, name, embedding_bytes, faiss_index_bytes ,text_content) 
                    VALUES(?, ?, ?, ?, ?, ?)
                """, (doc_id, db_id, doc_name, sqlite3.Binary(nembedding_bytes), sqlite3.Binary(faiss_index_bytes), text_json))
                
                print(f"(Debug) Successfully inserted document into database")
            except sqlite3.Error as e:
                print(f"(Debug) SQLite error during insert: {str(e)}")
                return {"error": f"Database error: {str(e)}"}

            print(f"(Debug) Successfully saved document {doc_id}")
            return {"message": "Document saved successfully", "doc_id": doc_id}
            
    except Exception as e:
        print(f"(Debug) Unexpected error in save_embedding: {str(e)}")
        return {"error": f"Failed to save document: {str(e)}"}
