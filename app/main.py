from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel
from app.db.models.user_model import User
from contextlib import asynccontextmanager

data_base_URL = "sqlite:///./gym.db"
engine = create_engine(data_base_URL, connect_args= {"check_same_thread": False})

def create_db_and_tables():
    print("Running create_db_and_tables")
    SQLModel.metadata.create_all(engine)

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

@app.get('/')
def home() -> dict :
    return {"Message": "Welcome"}