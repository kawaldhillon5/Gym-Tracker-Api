from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    user_name: str
    email: str
    password: str = Field(max_length=72)