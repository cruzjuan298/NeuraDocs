import os
from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path

uploadRouter = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@uploadRouter.post("/upload")
async def upload_document(db_id: str = Form(...), file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    from app.services.parse import parse_doc
    ## text is the formatted text and doc_info is the normal text 
    text, docInfo = parse_doc(file_path)
    print(text)
    from app.services.embedding import process_file
    doc_id = process_file(db_id, file.filename, docInfo, text)
    
    return {"message" : "Document processed", "doc_id": doc_id, "db_id" : db_id}