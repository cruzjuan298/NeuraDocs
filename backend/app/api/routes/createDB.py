from fastapi import APIRouter
from pydantic import BaseModel

createDBRouter = APIRouter()

class CreateDB(BaseModel):
    dbId: str
    dbName: str

@createDBRouter.post("/createDB")
async def createNewDB(create: CreateDB):
    from app.services.storage import insertDb
    message = insertDb(create.dbId, create.dbName)
    print(message)
    if insertDb is None:
        return None
    return {"message" : message}