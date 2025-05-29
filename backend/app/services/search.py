import faiss
import numpy as np
import pickle
from .embedding import model 
from .retrieval import getDbEmbeddings, getDocIdsByDbId, getInfo
from .transform import blobToEmbedding


def get_query_embedding(query: str):
     query_embedding = model.encode(query).astype("float32").reshape(1, -1)
     return query_embedding

def find_best_match(query: str, db_id: str):
    try:
        query_embedding = get_query_embedding(query)

        dbEmbeddings = getDbEmbeddings(db_id)
        doc_ids = getDocIdsByDbId(db_id)

        if not dbEmbeddings or not doc_ids:
            return {"error": "No documents found in database"}

        embeddingsList = []
        for embedding in dbEmbeddings:
            originalEmbeddingArray = blobToEmbedding(embedding)
            embeddingsList.append(originalEmbeddingArray)

        if not embeddingsList:
            return {"error": "No valid embeddings found"}

        embeddings_np = np.vstack(embeddingsList).astype("float32")

        index = faiss.IndexFlatL2(embeddings_np.shape[1])
        index.add(embeddings_np)

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
        return {"error": f"Search failed in find_best_match: {str(e)}"}
    
def find_best_sentence(query: str, db_id: str, doc_id: str):
    try:
        query_embedding = get_query_embedding(query)

        # getInfo returns a tuple of (doc_id, doc_name, embedding, faissIndex)
        doc_info = getInfo(db_id, doc_id)
        
        if doc_info is None:
            return {"error": "Document not found"}
            
        doc_id, doc_name, embedding, faiss_index, text_content = doc_info
        
        if faiss_index is None:
            return {"error": "Document has no sentence embeddings available for search"}
            
        sentIndexDeserialized = pickle.loads(faiss_index)

        distance, indicies = sentIndexDeserialized.search(query_embedding, k=1)
        
        bestMatchIndex = indicies[0][0]

        bestMatchSentence = text_content[bestMatchIndex]

        return {
            "doc_id": doc_id,
            "doc_name": doc_name,
            "embedding": embedding.tolist(),  # convert numpy array to list for JSON serialization
            "faiss_index": faiss_index,
            "text_content": text_content, 
            "best_match_sentence" : bestMatchSentence
        }

    except Exception as e:
        print(f"Error in finding the relevant info in the doc: {str(e)}")
        return {"error": f"Search failed in find_best_sentence: {str(e)}"}
