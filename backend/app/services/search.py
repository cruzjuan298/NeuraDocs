import os
import json
import faiss
import numpy as np
from app.assets.model import model
from .retrieval import getDbEmbeddings, getDocIdsByDbId, getInfo
from .transform import blobToEmbedding

# here we are deserializing the bytes data to a byte stream using the io modules ByteIO method. Then we just load index object using the write_index method and return it. 
## documentation used => https://docs.python.org/3/library/io.html
def deserialize_from_bytes(faiss_index_bytes):
    if not isinstance(faiss_index_bytes, bytes):
        raise TypeError(f"Expected a byte type for the faiss index. Got {type(faiss_index_bytes)}")
    
    temp_file = "deserialize_index.faiss"
    index = None

    try:
        with open(temp_file, "wb") as f:
            f.write(faiss_index_bytes)
        index = faiss.read_index(temp_file)

    except Exception as e:
        print(f"Error during FAISS deserialization via file: {str(e)}")
        raise
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return index

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
    

## to find the best sentence, the embeddings of the whole document isn't needed, just the faiss index of the sentences is. 
def find_best_sentence(query: str, db_id: str, doc_id: str):
    try:
        query_embedding = get_query_embedding(query)

        # getInfo returns a tuple of (faissIndex, textContent)
        doc_info = getInfo(db_id, doc_id)
        
        if doc_info is None:
            return {"error": "Document not found"}
            
        ndoc_id, doc_name, embedding, faiss_index_bytes, text_content_json = doc_info

        if faiss_index_bytes is None:
            return {"error": "Document has no sentence embeddings available for search"}
            
        deserialized_index = deserialize_from_bytes(faiss_index_bytes)

        distances, indices = deserialized_index.search(query_embedding, k=1)

        best_match_index = indices[0][0]

        text_content = json.loads(text_content_json)

        if best_match_index >= len(text_content):
            return {"error" : f"Invalid index {best_match_index} for sentences of the document of length of {len(text_content)}"}

        best_match_sentence = text_content[best_match_index]
        
        return {
            "best_match_sentence" : best_match_sentence,
            "best_match_doc_name" : doc_name
        }

    except Exception as e:
        print(f"Error in finding the relevant info in the doc: {str(e)}")
        return {"error": f"Search failed in find_best_sentence: {str(e)}"}
