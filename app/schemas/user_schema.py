from pydantic import BaseModel, Field
from sqlmodel import SQLModel

class UserCreate(BaseModel):
    user_name: str
    email: str
    password: str = Field(max_length=72)

class UserRead( BaseModel):
    id: int
    user_name: str

class UserLogin(BaseModel):
    user_name:str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_name: str | None = None