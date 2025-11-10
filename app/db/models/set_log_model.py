from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .exercise_log_model import ExerciseLog

class SetLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    set_number: int
    reps: int
    weight_kg: float
    comment: Optional[str] 
    exercise_log_id: int = Field(foreign_key="exerciselog.id")
    exercise_log: "ExerciseLog" = Relationship(back_populates="set_logs")