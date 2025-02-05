from fastapi import FastAPI
from api.routes.upload import uploadRouter 
from api.routes.query import queryRouter

app = FastAPI()

app.include_router(uploadRouter, prefix="/files")
app.include_router(queryRouter, prefix="/query")