from sqlmodel import create_engine, SQLModel, Session

import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")

if database_url:

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    engine = create_engine(database_url, echo=False)
else:

    sqlite_file_name = "gym.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session