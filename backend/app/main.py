from fastapi import FastAPI
from app.api.routes.upload import uploadRouter 
from app.api.routes.query import queryRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(uploadRouter, prefix="/files")
app.include_router(queryRouter, prefix="/query")