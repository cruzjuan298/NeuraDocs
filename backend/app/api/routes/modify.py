from fastapi import APIRouter

modifyRouter = APIRouter()

@modifyRouter.put("/upload {doc_id}")
async def modifyDoc(doc_id):
    pass

@modifyRouter.patch("/update-db-name")
async def updateDbName(db_id: str, new_name: str):
  pass
