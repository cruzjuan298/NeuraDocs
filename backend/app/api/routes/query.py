from fastapi import APIRouter

queryRouter = APIRouter()

@queryRouter.get("/search")
def search(query: str):
    from app.services.search import find_best_match
    best_match = find_best_match(query)
    return {"best match": best_match}