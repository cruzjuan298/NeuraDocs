from fastapi import FastAPI
from app.api.routes.upload import uploadRouter 
from app.api.routes.query import queryRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(

    ##allowing for frontend and backend interacting)
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],

)

##api endpoints pre-fixes: /file/upload for uploading docs and /query/search for searching

app.include_router(uploadRouter, prefix="/files")
app.include_router(queryRouter, prefix="/query")