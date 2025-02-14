import faiss
import numpy as np

def find_best_match(query):
    from app.services.embedding import model 
    from app.services.storage import index, get_embedding, doc_id_mapping, get_document_text

    query_embedding = model.encode(query).astype("float32").reshape(1, -1)
    _, cloest_id = index.search(query_embedding, k=1)

    print(f"Number of entries in FAISS index:", index.ntotal)
    print(cloest_id)

    faiss_index = int(cloest_id[0][0])

    doc_id = None
    for key, value in doc_id_mapping.items():
        if value == faiss_index:
            doc_id = key
            break

    print(f"Closest ID returned by FAISS: {doc_id}")

    if doc_id is None:
        return {"error": f"No doc_id found for FAISS index {faiss_index}"}
    
    doc_metadata = get_embedding(doc_id)
    doc_text = get_document_text(doc_id)

    if doc_metadata and doc_text:
        return {"best_match" : doc_text}
    else:
        return {"error": "No matching document found."}
 