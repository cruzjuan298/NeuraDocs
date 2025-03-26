import sqlite3
import numpy as np

from app.services.storage import conn, cur

def getInfo(db_id: str ,doc_id: str):
    if not isinstance(doc_id, str):
        doc_id = str(doc_id)

    cur.execute("SELECT doc_id, name, embedding_bytes, faiss_index FROM document_metadata WHERE doc_id=? and db_id=?", (doc_id, db_id))
    
    result = cur.fetchone()

    if result:
        ndoc_id, doc_name, embedding_bytes, faissIndex = result
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        return ndoc_id, doc_name, embedding, faissIndex
    else:
        return None
    
def getDocId(db_id: str, docName: str):
    if not isinstance(docName, str):
        docName = str(docName)
    cur.execute("SELECT doc_id from document_metadata WHERE name=? AND db_id=?", (docName, db_id))
    result = cur.fetchone()

    if result:
        return result[0]
    else:
        return None


def getDb(db_id: str):
    if not isinstance(db_id, str):  
        db_id = str(db_id)
    
    cur.execute("SELECT * FROM document_metadata where db_id=?", (db_id,))
    results = cur.fetchall()
    
    if results:
        return results
    else:
        return None

def getDocNames(dbInfo):
    docNames = []
    for x in dbInfo:
        docNames.append(x[2])
    
    return docNames