from fastapi import FastAPI
from app.api.routes.upload import uploadRouter 
from app.api.routes.query import queryRouter

app = FastAPI()

app.include_router(uploadRouter, prefix="/files")
app.include_router(queryRouter, prefix="/query")