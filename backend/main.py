import os
import uvicorn
from fastapi import FastAPI
from app.api.routes.upload import uploadRouter 
from app.api.routes.query import queryRouter
from app.api.routes.retrieve import retrieveRouter
from app.api.routes.createDB import createDBRouter
from app.api.routes.modify import modifyRouter
from fastapi.middleware.cors import CORSMiddleware
from app.db.creaetDatabase import create_db
from dotenv import load_dotenv, dotenv_values
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app : FastAPI):
    db_status = create_db()
    if not db_status['success']:
        print(f"Error: Database intialization failed: {db_status['error']}")
        exit(1)
    print("Database initalized successfully")

    yield
    print("Application shutdown")

load_dotenv()

port = os.getenv("PORT")
frontend_baseUrl = os.getenv("FRONTEND_BASE_URL")


app = FastAPI(
    title="RAG documentation management backend",
    description="Easily extract data from all of your documents in one place",
    version="0.0.1",
    lifespan=lifespan
)

app.add_middleware(

    ##allowing for frontend and backend interacting
    CORSMiddleware,
    allow_origins=[frontend_baseUrl, f"http://127.0.0.1:{port}"], ## server might run on a different port is the port listed in your .env file is in use. To avoid this, check if the correct ports are being used
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],

)

##api endpoints pre-fixes: /file/upload for uploading docs and /query/search for searching

app.include_router(uploadRouter, prefix="/files")
app.include_router(queryRouter, prefix="/query")
app.include_router(retrieveRouter, prefix="/retrieve")
app.include_router(createDBRouter, prefix="/create")
app.include_router(modifyRouter, prefix="/modify")