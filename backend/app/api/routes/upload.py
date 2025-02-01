from fastapi import APIRouter, UploadFile, File
from app.services.embedding import process_document

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    doc_id = process_document(file.filename, text)
    return {"message" : "Document processed", "doc_id": doc_id}