from fastapi import APIRouter

createDBRouter = APIRouter()

@createDBRouter.post("/createDB")
def createNewDB(dbId):
    #inserting db id into the database

    from app.services.storage import insertDb
    insertDb(dbId)
    return {"message" : "Database inserted"}