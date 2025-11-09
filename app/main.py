from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db.models.user_model import User
from .db.models.check_in import CheckIn  
from contextlib import asynccontextmanager
from app.db.sqlite import create_db_and_tables
from app.routers import auth_router, check_in_router
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],    
)



app.include_router(auth_router.router)
app.include_router(check_in_router.router)


@app.get('/')
def home() -> dict :
    return {"Message": "Welcome"}