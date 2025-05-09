import faiss
import numpy as np

def find_best_match(query, db_id):
    from app.services.embedding import model 
    from app.services.storage import doc_index, doc_id_mapping
    from app.services.retrieval import getDb, getDbEmbeddings

    ## finds the best match by: creating an embedding of the queqry -> retrieve all embeddings of the doc -> gets the best match index -> gets the doc info from the db -> gets best match relevant info 

    query_embedding = model.encode(query).astype("float32").reshape(1, -1)

    db = getDb(db_id)

    dbEmbeddings = getDbEmbeddings(db_id)

    

    print(f"Number of entries in FAISS index:", doc_index.ntotal)

    faiss_index = int(cloest_id[0][0])

    doc_id = None
    for key, value in doc_id_mapping.items():
        if value == faiss_index:
            doc_id = key
            break

    print(f"Closest ID returned by FAISS: {doc_id}")

    if doc_id is None:
        return {"error": f"No doc_id found for FAISS index {faiss_index}"}
    

 