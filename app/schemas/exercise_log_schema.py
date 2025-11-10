from sqlmodel import SQLModel
from set_log_schema import SetLogRead

class ExerciseLogBase(SQLModel):
    exercise_name: str

# The "Create" schema
class ExerciseLogCreate(ExerciseLogBase):
    workout_id: int

# The "Read" schema: This is nested!
# It returns the Exercise... *with all of its sets*
class ExerciseLogRead(ExerciseLogBase):
    id: int
    set_logs: list[SetLogRead] = []