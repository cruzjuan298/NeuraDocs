from fastapi import APIRouter

createDBRouter = APIRouter()

@createDBRouter.post("/createDB")
def createNewDB(dbId, db_name):
    from app.services.storage import insertDb
    if not isinstance(dbId, str) and not isinstance(db_name, str):
        dbId = str(dbId)
        db_name = str(db_name)
    message = insertDb(dbId, db_name)
    print(message)
    if insertDb is None:
        return None
    return {"message" : message}