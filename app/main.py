from fastapi import FastAPI, Request
from typing import Optional
from sqlmodel import Field, Session, SQLModel

app = FastAPI(
    title="Gym Tracker API"    
)

@app.get('/')
def home() -> dict :
    return {"Message": "Welcome"}