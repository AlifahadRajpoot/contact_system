from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
from config.db import create_tables
from routes import user_routes,contact_routes

@asynccontextmanager
async def lifespan(app:FastAPI):
    
    print("App is starting up...")
    
    create_tables()
    yield
    
    print("App is shuting down...")
    
app=FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

app.include_router(user_routes.user_router,prefix="/user",tags=["User"])
app.include_router(contact_routes.contact_router,prefix="/contact",tags=["Contact"])

def start():
    uvicorn.run("contact_system.main:app",host="127.0.0.1",port=8000,reload=True)