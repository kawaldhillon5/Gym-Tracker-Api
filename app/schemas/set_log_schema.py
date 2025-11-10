from sqlmodel import SQLModel
from typing import Optional

class SetLogBase(SQLModel):
    set_number: int
    reps: int
    weight_kg: float
    comment : Optional[str]

class SetLogCreate(SetLogBase):
    exercise_log_id: int

class SetLogRead(SetLogBase):
    id: int
