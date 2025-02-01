import faiss
import hashlib
import numpy as np
from sentence_transformers import SentenceTransformer
from app.services.storage import save_embedding, get_embedding

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def hash_text(text) :
    ##creating a hash to prevent duplication in the embeddedings
    return hashlib.sha256(text.encode()).hexdigest()

def process_doc(doc_id, text):
    doc_id = hash_text(text)

    exisiting_embedding = get_embedding(doc_id)

    if exisiting_embedding is not None:
        return doc_id
    
    embedding = model.encode(text).astype("float32").reshape(1, -1)

    save_embedding(doc_id, doc_name, embedding)

    return doc_id

