import faiss
import numpy as np

def find_best_match(query):
    from app.services.embedding import model 
    from app.services.storage import index, get_embedding

    query_embedding = model.encode(query).astype("float32").reshape(1, -1)
    _, cloest_id = index.search(query_embedding, k=1)

    print(cloest_id)
    doc_id = str(cloest_id[0][0])

    doc_metadata = get_embedding(doc_id)

    if doc_metadata:
        doc_id, doc_name, embedding = doc_metadata
        return {"best_match" : {"doc_id": doc_id, "doc_name" : doc_name, "embedding" : embedding.tolist()}}
    else:
        return {"error": "No matching document found."}