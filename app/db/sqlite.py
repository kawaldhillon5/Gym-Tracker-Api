from sqlmodel import create_engine, SQLModel, Session

import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

data_base_URL = DATABASE_URL
engine = create_engine(data_base_URL, connect_args= {"check_same_thread": False}) #type: ignore

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session