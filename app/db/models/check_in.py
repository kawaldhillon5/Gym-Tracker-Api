from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import date

class CheckIn(SQLModel, table = True):
    id : Optional[int] =  Field(default = None, primary_key=True)
    check_in_date: date = Field(index=True)
    user_id : int = Field(foreign_key="user.id")