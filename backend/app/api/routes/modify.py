from fastapi import APIRouter
from app.services.storage import conn, cur

modifyRouter = APIRouter()

@modifyRouter.put("/upload {doc_id}")
async def modifyDoc(doc_id):
    pass

@modifyRouter.patch("/update-db-name")
async def updateDbName(db_id: str, new_name: str):
    try:
        cur.execute("UPDATE document SET name = ? WHERE db_id = ?", (new_name, db_id))
        conn.commit()
        return {"message": "Database name updated successfully"}
    except Exception as e:
        return {"error": str(e)}
