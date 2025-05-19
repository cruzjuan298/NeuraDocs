import faiss
import numpy as np
from app.services.embedding import model 
from app.services.retrieval import getDbEmbeddings, getDocIdsByDbId
from app.services.transform import blobToEmbedding


def find_best_match(query, db_id):
    try:
        # Create query embedding
        query_embedding = model.encode(query).astype("float32").reshape(1, -1)

        # Get database embeddings and doc IDs
        dbEmbeddings = getDbEmbeddings(db_id)
        doc_ids = getDocIdsByDbId(db_id)

        if not dbEmbeddings or not doc_ids:
            return {"error": "No documents found in database"}

        # Convert embeddings to numpy arrays
        embeddingsList = []
        for embedding in dbEmbeddings:
            originalEmbeddingArray = blobToEmbedding(embedding)
            embeddingsList.append(originalEmbeddingArray)

        if not embeddingsList:
            return {"error": "No valid embeddings found"}

        # Convert list to numpy array
        embeddings_np = np.vstack(embeddingsList).astype("float32")

        # Build FAISS index
        index = faiss.IndexFlatL2(embeddings_np.shape[1])
        index.add(embeddings_np)

        # Search for nearest neighbor
        distances, indices = index.search(query_embedding, k=1)
        
        if indices.size == 0:
            return {"error": "No matches found"}

        faiss_index = indices[0][0]
        
        if faiss_index >= len(doc_ids):
            return {"error": f"Invalid index {faiss_index} for document list of length {len(doc_ids)}"}

        doc_id = doc_ids[faiss_index]
        print(f"Closest ID returned by FAISS: {doc_id}")

        return {
            "doc_id": doc_id,
            "distance": float(distances[0][0])  # Convert numpy float to Python float
        }

    except Exception as e:
        print(f"Error in find_best_match: {str(e)}")
        return {"error": f"Search failed: {str(e)}"}
    

 