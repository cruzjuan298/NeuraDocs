from fastapi import APIRouter
from app.services.retrieval import getDocId, getDb, getDocNames

retrieveRouter = APIRouter()

##retrieve methods for getting database or doc info

@retrieveRouter.get("/retrieve")
async def retrieveDb(db_id: str) :
    dbInfo = getDb(db_id)
    dbDocNames = getDocNames(dbInfo)
    return dbDocNames

@retrieveRouter.get("/retrieveDoc")
async def getDoc(db_id, docName):
    docId = getDocId(db_id, docName)

    if docId is None:
        return {"message" : "Document not found"}
    
    return {"doc_id" : docId}


@retrieveRouter.get("/retreiveDatabase")
async def getDB(db_id, docName):
    docId = getDocId(db_id, docName)

    if docId is None:
        return {"message" : "Document not found"}
    
    return {"doc_id" : docId}
