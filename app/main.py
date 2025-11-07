from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db.models.user_model import User
from contextlib import asynccontextmanager
from app.db.sqlite import create_db_and_tables
from app.routers import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown
    print("Shut Down")

app = FastAPI(
    title="Gym Tracker API",
    lifespan = lifespan    
)

app.include_router(auth_router.router)

@app.get('/')
def home() -> dict :
    return {"Message": "Welcome"}