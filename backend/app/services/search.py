import faiss
import numpy as np

def find_best_match(query, db_id):
    from app.services.embedding import model 
    from app.services.retrieval import getDbEmbeddings, getDocIdsByDbId
    from app.services.transform import blobToEmbedding
    ## finds the best match by: creating an embedding of the queqry -> retrieve all embeddings of the doc -> gets the best match index -> gets the doc info from the db -> gets best match relevant info 

    query_embedding = model.encode(query).astype("float32").reshape(1, -1)

    dbEmbeddings = getDbEmbeddings(db_id)
    doc_ids = getDocIdsByDbId(db_id)

    faiss_index = 0
    doc_id = None

    if dbEmbeddings:
        embeddingsList = []
        for embedding in dbEmbeddings:
            originalEmbeddingArray = blobToEmbedding(embedding)
            embeddingsList.append(originalEmbeddingArray)

        if embeddingsList:
                # TODO find cloesest matching ID out of the embedding bytes and then get the relevant info
              embeddings_np = np.array(embeddingsList).astype("float32")

              # building faiss index
              index = faiss.IndexFlatL2(embeddings_np.shape[1])
              index.add(embeddings_np)


              d, i = index.search(query_embedding, k=1)

              faiss_index = i[0][0]

              if faiss_index < len(embeddingsList):
                  doc_id = doc_ids[faiss_index]

    print(f"Closest ID returned by FAISS: {doc_id}")

    if doc_id is None:
        return {"error": f"No doc_id found for FAISS index {faiss_index}"}
    
    return {"doc_id": doc_id}
    

 