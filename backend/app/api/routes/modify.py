from fastapi import APIRouter
from app.services.modify import modifyName 

modifyRouter = APIRouter()

@modifyRouter.put("/upload {doc_id}")
def modifyDoc(doc_id):
  pass

@modifyRouter.patch("/update-db-name")
def updateDbName(db_id: str, new_name: str):
  result = modifyName(db_id, new_name)
    
  return result 
