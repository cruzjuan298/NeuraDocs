from fastapi import APIRouter, Query
from app.services.retrieval import getDocId, getDb, getDocNames

retrieveRouter = APIRouter()

##retrieve methods for getting database or doc info

@retrieveRouter.get("/retrieveDatabase")
async def retrieveDb(db_id: str) :
    if not isinstance(db_id, str):
        db_id = str(db_id)
    
    dbInfo = getDb(db_id)
    if dbInfo is None:
        return None

    dbDocNames = getDocNames(dbInfo)
    return {"doc_names" :  dbDocNames}

@retrieveRouter.get("/retrieveDoc")
async def getDoc(db_id, docName):
    docId = getDocId(db_id, docName)
    
    if docId is None:
        return {"message" : "Document not found"}
    
    return {"doc_id" : docId}
