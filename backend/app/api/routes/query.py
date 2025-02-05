from fastapi import APIRouter
from app.services.search import find_best_match

queryRouter = APIRouter()

@queryRouter.get("/search")
def search(query: str):
    best_match = find_best_match(query)
    return {"best match": best_match}