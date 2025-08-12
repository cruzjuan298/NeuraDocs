from fastapi import APIRouter
import numpy as np
from pydantic import BaseModel

queryRouter = APIRouter()

class SearchRequest(BaseModel):
    query: str
    db_id: str

@queryRouter.post("/search")
def search(request: SearchRequest):
    try:
        from app.services.search import find_best_match, find_best_sentence

        best_match_doc = find_best_match(request.query, request.db_id)
        
        if "error" in best_match_doc:
            return best_match_doc

        best_match = find_best_sentence(
            request.query, 
            request.db_id, 
            best_match_doc["doc_id"]
        )

        if "error" in best_match:
            return best_match

        return {
            "best_match": best_match,
            "document_match": best_match_doc
        }
    
    except Exception as e:
        print(f"Error in search endpoint: {str(e)}")
        return {"error": str(e)}