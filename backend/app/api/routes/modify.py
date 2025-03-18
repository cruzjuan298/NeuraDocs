from fastapi import APIRouter

modifyRouter = APIRouter()

@modifyRouter.put("/upload {doc_id}")
async def modifyDoc(doc_id):
    pass
