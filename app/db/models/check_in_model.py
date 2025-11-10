from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import date

if TYPE_CHECKING:
    from .user_model import User
    from .workout_model import Workout


class CheckIn(SQLModel, table = True):
    id : Optional[int] =  Field(default = None, primary_key=True)
    check_in_date: date = Field(index=True)
    user_id : int = Field(foreign_key="user.id")
    workout: Optional["Workout"] = Relationship(
        back_populates="check_in", 
        sa_relationship_kwargs={"uselist": False}
    )    