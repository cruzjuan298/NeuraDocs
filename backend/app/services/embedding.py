import faiss
import hashlib
import numpy as np
from app.assets.model import model

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

    sentence_embedding = model.encode(text, convert_to_numpy=True)
    result = save_embedding(db_id, doc_id, doc_name, text, sentence_embedding)
    print(result)
    return doc_id

def generateEmbeding(item):
    items_embeddings = model.encode(item, convert_to_numpy=True)
    return items_embeddings