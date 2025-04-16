import faiss
import hashlib
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def hash_doc(doc) :
    ##creating a hash to prevent duplication in the embeddedings
    return hashlib.sha256(doc.encode()).hexdigest()

def process_file(db_id, doc_name, doc_info, text):
    doc_id = hash_doc(doc_info)
    print(f"Doc id from uploaded doc: ${doc_id}")

    from app.services.storage import save_embedding, insertDb
    from app.services.retrieval import getInfo, getDb

    ## checking is the document has already been proccessed
    exisiting_info = getInfo(db_id, doc_id)
    if exisiting_info is not None:
        return doc_id
    
    exisitingDb = getDb(db_id)
    if exisitingDb is None:
        insertDb(db_id, doc_name)

    embedding = model.encode(doc_info).astype("float32").reshape(1, -1)
    sentence_embedding = model.encode(text, convert_to_numpy=True)
    save_embedding(db_id, doc_id, doc_name, embedding, text, sentence_embedding)
    
    return doc_id

