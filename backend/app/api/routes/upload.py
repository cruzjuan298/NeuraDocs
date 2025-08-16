import os
from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path

uploadRouter = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@uploadRouter.post("/upload")
async def upload_document(db_id: str = Form(...), file: UploadFile = File(...)):
    print(f"(Debug) Starting upload for db_id: {db_id}, file: {file.filename}")

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())
    print(f"(Debug) File saved to: {file_path}")

    from app.services.parse import parse_doc
    ## text is the formatted text and doc_info is the normal text 
    text, docInfo = parse_doc(file_path)
    print(f"(Debug) Parsed document - text length: {len(text)}, docInfo length: {len(docInfo)}")
    
    from app.services.embedding import process_file
    ## once again 
    doc_id = process_file(db_id, file.filename, docInfo, text)
    print(f"(Debug) Document processed - doc_id: {doc_id}")
    
    ##for testing purposes only: checking if doc was added
    from app.services.retrieval import getInfo
    doc_info = getInfo(db_id, doc_id)
    print(f"(Debug) Document verification - exists in database: {doc_info is not None}")
    
    return {"message" : "Document processed", "doc_id": doc_id, "db_id" : db_id}