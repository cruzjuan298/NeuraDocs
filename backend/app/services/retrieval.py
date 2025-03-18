import sqlite3
import numpy as np

from app.services.storage import conn, cur

def getInfo(doc_id):
    if not isinstance(doc_id, str):
        doc_id = str(doc_id)

    cur.execute("SELECT doc_id, name, embedding_bytes, faiss_index FROM document WHERE doc_id=?", (doc_id,))
    
    result = cur.fetchone()

    if result:
        ndoc_id, doc_name, embedding_bytes, faissIndex = result
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        return ndoc_id, doc_name, embedding, faissIndex
    else:
        return None
    
def getDocId(docName):
    if not isinstance(docName, str):
        docName = str(docName)
    cur.execute("SELECT doc_id from document WHERE name=?", (docName,))
    result = cur.fetchone()

    if result:
        return result
    else:
        return None 