from fastapi import APIRouter

createDBRouter = APIRouter()

@createDBRouter.post("/createDB")
def createNewDB(dbId):
    #inserting db id into the database
    from app.services.storage import insertDb
    message = insertDb(dbId)
    if insertDb is None:
        return None
    return {"message" : message}