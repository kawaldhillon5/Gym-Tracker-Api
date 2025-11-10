from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .workout_model import Workout
    from .set_log_model import SetLog

class ExerciseLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exercise_name: str = Field(index=True)
    workout_id: int = Field(foreign_key="workout.id")
    workout: "Workout" = Relationship(back_populates="exercise_logs")
    set_logs: list["SetLog"] = Relationship(back_populates="exercise_log")