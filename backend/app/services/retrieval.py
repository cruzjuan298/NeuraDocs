import sqlite3
import numpy as np
import json

from app.db.connection import get_db_connection

def getInfo(db_id: str ,doc_id: str):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

            print(f"(Debug) Getting info for doc_id: {doc_id}, db_id: {db_id}")
            if not isinstance(doc_id, str):
                doc_id = str(doc_id)

            cur.execute("SELECT doc_id, name, faiss_index_bytes, text_content FROM document_metadata WHERE doc_id=? and db_id=?", (doc_id, db_id))
            
            result = cur.fetchone()
            print(f"(Debug) Query result: {result is not None}")

            if result:
                ndoc_id, doc_name, faiss_index_bytes, text_content = result
                print(f"(Debug) Successfully retrieved document info for: {doc_name}")
                return ndoc_id, doc_name, faiss_index_bytes, text_content
            else:
                print(f"(Debug) No document found with doc_id: {doc_id} and db_id: {db_id}")
                return None
    except Exception as e:
        print(f"Error occurred while trying to get info for doc id: {doc_id} -> Error: {str(e)}")
        return None
    
def getDocId(db_id: str, docName: str):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

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
    except Exception as e:
        print(f"Error in trying to get doc info. Error: {str(e)}")
        return None

def getDb(db_id: str):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

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
                return [] 
    except Exception as e:
        print(f"Error when trying to get db by db id: {db_id}. Error: {str(e)}")
        return None

def getDocNames(dbInfo):
    docNames = []
    for x in dbInfo:
        docNames.append(x[2])
    
    return docNames

## this is different than getDb since this only gets doc_id from the db_id associated with it instead of the whole db 
def getDocIdsByDbId(db_id: str):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

            cur.execute("SELECT doc_id FROM document_metadata WHERE db_id=? ORDER BY ROWID", (db_id,))
            results = cur.fetchall()
            return [row[0] for row in results]
    except Exception as e:
        print(f"Error while trying to get doc by db id: {str(e)}")


def getDocText(doc_id: str) -> list:
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

            cur.execute("SELECT text_content FROM document_metadata WHERE doc_id=?", (doc_id,))
            result = cur.fetchone()
            if result and result[0]:
                return json.loads(result[0])
            return None
    except Exception as e:
        print(f"Error retrieving document text: {str(e)}")
        return None

def getAllDb():
    try:
        with get_db_connection() as conn:
            dbs = []
            cur = conn.cursor()

            cur.execute("SELECT * FROM document")
            result = cur.fetchall()

            if result:
                dbs = [{"db_id" : row[0], "name" : row[1]} for row in result]
                return dbs
            else:
                return []
    except Exception as e:
        return None
    

def getDocNamesFromDb(db_id):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

            cur.execute("SELECT name FROM document_metadata WHERE db_id=?", (db_id,))

            result = cur.fetchall()

            if result:
                docNames = [row[0] for row in result]
                return docNames
            return []
    except Exception as e:
        print("Error occured while trying to get doc names from db")
        return None