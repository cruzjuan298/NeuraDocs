import os
from fastapi import APIRouter, UploadFile, File
from pathlib import Path

uploadRouter = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@uploadRouter.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    from app.services.parse import parse_doc
    text = parse_doc(file_path)
    print(text)
    from app.services.embedding import process_doc
    doc_id = process_doc(file.filename, text)
    
    return {"message" : "Document processed", "doc_id": doc_id}