from fastapi import APIRouter
from app.services.deleteItems import deleteDbPerm
deleteRouter = APIRouter()

@deleteRouter.delete("/removeDb")
async def deleteDb(db_id: str):
    return deleteDbPerm(db_id)