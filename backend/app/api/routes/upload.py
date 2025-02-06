from fastapi import APIRouter, UploadFile, File

uploadRouter = APIRouter()

@uploadRouter.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("latin-1")
    from app.services.embedding import process_document
    doc_id = process_document(file.filename, text)
    return {"message" : "Document processed", "doc_id": doc_id}