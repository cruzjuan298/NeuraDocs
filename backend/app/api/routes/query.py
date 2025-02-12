from fastapi import APIRouter
import numpy as np
queryRouter = APIRouter()

@queryRouter.post("/search")
async def search(query: str):
    from app.services.search import find_best_match
    result = find_best_match(query)

    return result