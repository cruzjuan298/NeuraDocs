from fastapi import APIRouter
from app.services.retrieval import getDocId, getInfo

retrieveRouter = APIRouter()

##retrieve methods for getting database or doc info

@retrieveRouter.get("/retrieve")
async def retrieveDoc(docName) :
    docId = getDocId(docName)

    if docId is None:
        return {"message" : "Document not found"}

    docInfo = getInfo(docId)
    return {"message" : "request processed", "doc_id" : docInfo[0], "doc_name" : docInfo[1], "doc_embedding" : docInfo[2], "doc_faissIndex" : docInfo[3]}

@retrieveRouter.get("/retrieveDoc")
async def getDoc(docName):
    docId= getDocId(docName)

    if docId is None:
        return {"message" : "Document not found"}
    return {"doc_id" : docId}


@retrieveRouter.get("/retreiveDatabase")
async def getDB(docName):
    docId = getDocId(docName)

    if docId is None:
        return {"message" : "Document not found"}
    return {"doc_id" : docId}
