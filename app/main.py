from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db.models.user_model import User
from app.db.models.check_in_model import CheckIn
from app.db.models.workout_model import Workout
from app.db.models.exercise_log_model import ExerciseLog
from app.db.models.set_log_model import SetLog  
from contextlib import asynccontextmanager
from app.db.sqlite import create_db_and_tables
from app.routers import auth_router, check_in_router, workout_router
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv

load_dotenv()

ORIGIN  = os.getenv("ORIGIN")



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
   ORIGIN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # type: ignore 
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],    
)



app.include_router(auth_router.router)
app.include_router(check_in_router.router)
app.include_router(workout_router.router)


@app.get('/')
def home() -> dict :
    return {"Message": "Welcome"}