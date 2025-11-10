from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .check_in_model import CheckIn
    from .exercise_log_model import ExerciseLog

class Workout(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default="My Workout")
    check_in_id: int = Field(foreign_key="checkin.id", unique=True)
    check_in: "CheckIn" = Relationship(back_populates="workout")
    exercise_logs: list["ExerciseLog"] = Relationship(back_populates="workout")