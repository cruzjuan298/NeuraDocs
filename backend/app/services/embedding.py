import faiss
import hashlib
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def hash_doc(doc) :
    ##creating a hash to prevent duplication in the embeddedings
    return hashlib.sha256(doc.encode()).hexdigest()

def process_file(doc_name, doc_info, text):
    doc_id = hash_doc(doc_info)
    print(f"Doc id from uploaded doc: ${doc_id}")

    from app.services.storage import save_embedding, get_embedding
    exisiting_embedding = get_embedding(doc_id)

    if exisiting_embedding is not None:
        return doc_id
    
    embedding = model.encode(doc_info).astype("float32").reshape(1, -1)
    sentence_embedding = model.encode(text, convert_to_numpy=True)
    save_embedding(doc_id, doc_name, embedding, text, sentence_embedding)
    
    return doc_id

