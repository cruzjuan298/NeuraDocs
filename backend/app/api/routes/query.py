from fastapi import APIRouter
import numpy as np
from pydantic import BaseModel

queryRouter = APIRouter()

class SearchRequest(BaseModel):
    query: str
    db_id: str

@queryRouter.post("/search")
async def search(request: SearchRequest):
    try:
        # For now, return a mock response
        # TODO Implement actual search functionality
        from app.services.search import find_best_match

        best_match = find_best_match(request.query, request.db_id)

        if best_match == None:
            return "No best match found"
        return {"best_match" : best_match}
    
    except Exception as e:
        return {"error": str(e)}