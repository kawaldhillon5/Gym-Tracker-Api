from sqlmodel import create_engine, SQLModel, Session

data_base_URL = "sqlite:///./gym.db"
engine = create_engine(data_base_URL, connect_args= {"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session