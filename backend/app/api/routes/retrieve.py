from fastapi import APIRouter, Query
from app.services.retrieval import getDocId, getDb, getDocNames

retrieveRouter = APIRouter()

##retrieve methods for getting database or doc info

@retrieveRouter.get("/retrieveDatabase")
async def retrieveDb(db_id: str) :
    print(f"(Debug) Retrieving database with db_id: {db_id}")
    if not isinstance(db_id, str):
        db_id = str(db_id)
    
    dbInfo = getDb(db_id)
    print(f"(Debug) Database info retrieved: {dbInfo is not None}")
    
    if dbInfo is None:
        print(f"(Debug) No database found for db_id: {db_id}")
        return None

    dbDocNames = getDocNames(dbInfo)
    print(f"(Debug) Found document names: {dbDocNames}")
    return {"doc_names" :  dbDocNames}

@retrieveRouter.get("/retrieveDoc")
async def getDoc(db_id, docName):
    print(f"(Debug) Retrieving document - db_id: {db_id}, docName: {docName}")
    docId = getDocId(db_id, docName)
    print(f"(Debug) Retrieved doc_id: {docId}")
    
    if docId is None:
        print(f"(Debug) Document not found - db_id: {db_id}, docName: {docName}")
        return {"message" : "Document not found"}
    
    return {"doc_id" : docId}
