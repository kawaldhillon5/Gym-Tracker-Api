from sqlmodel import SQLModel
from app.schemas.set_log_schema import SetLogRead

class ExerciseLogBase(SQLModel):
    exercise_name: str

class ExerciseLogCreate(ExerciseLogBase):
    workout_id: int

class ExerciseLogRead(ExerciseLogBase):
    id: int
    set_logs: list[SetLogRead] = []