import sqlite3
import numpy as np
import json

from app.services.storage import conn, cur

def getInfo(db_id: str ,doc_id: str):
    print(f"(Debug) Getting info for doc_id: {doc_id}, db_id: {db_id}")
    if not isinstance(doc_id, str):
        doc_id = str(doc_id)

    cur.execute("SELECT doc_id, name, embedding_bytes, faiss_index, text_content FROM document_metadata WHERE doc_id=? and db_id=?", (doc_id, db_id))
    
    result = cur.fetchone()
    print(f"(Debug) Query result: {result is not None}")

    if result:
        ndoc_id, doc_name, embedding_bytes, faissIndex, textContent = result
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        print(f"(Debug) Successfully retrieved document info for: {doc_name}")
        return ndoc_id, doc_name, embedding, faissIndex, textContent
    else:
        print(f"(Debug) No document found with doc_id: {doc_id} and db_id: {db_id}")
        return None
    
def getDocId(db_id: str, docName: str):
    print(f"(Debug) Getting doc_id for db_id: {db_id}, docName: {docName}")
    if not isinstance(docName, str):
        docName = str(docName)
    cur.execute("SELECT doc_id from document_metadata WHERE name=? AND db_id=?", (docName, db_id))
    result = cur.fetchone()
    print(f"(Debug) Query result: {result}")

    if result:
        print(f"(Debug) Found doc_id: {result[0]}")
        return result[0]
    else:
        print(f"(Debug) No document found with name: {docName} in db: {db_id}")
        return None


def getDb(db_id: str):
    print(f"(Debug) Getting database info for db_id: {db_id}")
    if not isinstance(db_id, str):  
        db_id = str(db_id)
    
    cur.execute("SELECT * FROM document_metadata where db_id=?", (db_id,))
    results = cur.fetchall()
    print(f"(Debug) Found {len(results) if results else 0} documents in database")

    if results:
        return results
    else:
        print(f"(Debug) No documents found in database for db_id: {db_id}")
        return None

def getDocNames(dbInfo):
    docNames = []
    for x in dbInfo:
        docNames.append(x[2])
    
    return docNames

def getDbEmbeddings(db_id: str): 
    if not isinstance(db_id, str ):
        db_id = str(db_id)
    
    cur.execute("SELECT embedding_bytes from document_metadata where db_id=?", (db_id,))
    results = cur.fetchall()
    
    if results:
        return [res[0] for res in results]
    else:
        return None


## this is different than getDb since this only gets doc_id from the db_id associated with it instead of the whole db 
def getDocIdsByDbId(db_id: str):
    cur.execute("SELECT doc_id FROM document_metadata WHERE db_id=? ORDER BY ROWID", (db_id,))
    results = cur.fetchall()
    return [row[0] for row in results]


def getDocText(doc_id: str) -> list:
    try:
        cur.execute("SELECT text_content FROM document_metadata WHERE doc_id=?", (doc_id,))
        result = cur.fetchone()
        if result and result[0]:
            return json.loads(result[0])
        return None
    except Exception as e:
        print(f"Error retrieving document text: {str(e)}")
        return None
