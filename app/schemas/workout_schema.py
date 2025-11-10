from sqlmodel import SQLModel
from app.schemas.exercise_log_schema import ExerciseLogRead 

class WorkoutBase(SQLModel):
    name: str | None = "My Workout"

class WorkoutCreate(WorkoutBase):
    check_in_id: int 

class WorkoutRead(WorkoutBase):
    id: int
    exercise_logs: list[ExerciseLogRead] = []