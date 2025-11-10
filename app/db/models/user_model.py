from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .check_in_model import CheckIn

class User(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(unique= True, index=True)
    email: str = Field(unique= True)
    hashed_password : str 
    check_ins: list["CheckIn"] = Relationship(back_populates="user")