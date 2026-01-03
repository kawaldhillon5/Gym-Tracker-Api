from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import date

from ..db.sqlite import get_session
from ..db.models.user_model import User
from ..db.models.check_in_model import CheckIn
from ..db.models.workout_model import Workout
from ..db.models.exercise_log_model import ExerciseLog
from ..db.models.set_log_model import SetLog 

from ..schemas.workout_schema import (WorkoutCreate, WorkoutRead)
from ..schemas.exercise_log_schema import (ExerciseLogCreate, ExerciseLogRead)
from .. schemas.set_log_schema import (SetLogCreate, SetLogRead, SetLogUpdate)

from ..security import get_current_user

router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.post('/', response_model=WorkoutRead)
def create_workout(workout_data: WorkoutCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    check_in = session.get(CheckIn, workout_data.check_in_id)
    if not check_in : 
        raise HTTPException(status_code=404, detail="Check In Not Found")
    
    assert current_user.id is not None
    if check_in.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this check-in.")
    
    if check_in.workout:
         raise HTTPException(status_code=409, detail="A workout already exists for this check-in.")
    
    new_workout = Workout.model_validate(workout_data)

    session.add(new_workout)
    session.commit()
    session.refresh(new_workout)

    return new_workout

@router.get('/checkin-info/{dateStr}', response_model=WorkoutRead)
def checkin_info(dateStr: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):

    query = select(CheckIn).where(CheckIn.user_id == current_user.id, CheckIn.check_in_date == dateStr)
    check_in = session.exec(query).first()

    if not check_in : 
        raise HTTPException(status_code=404, detail="Check In info not Found")
    
    assert current_user.id is not None
    if check_in.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this Info.")
    
    if not check_in.workout:
        raise HTTPException(status_code=404, detail="No Workout Data found")

    workout = check_in.workout
    return workout



@router.post("/exercise-logs/", response_model=ExerciseLogRead)
def create_exercise_log(exercise_data: ExerciseLogCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    workout = session.get(Workout, exercise_data.workout_id)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found.")

    assert workout.check_in.user_id is not None 
    if workout.check_in.user_id != current_user.id:
         raise HTTPException(status_code=403, detail="Not authorized to access this workout.")

    new_exercise_log = ExerciseLog.model_validate(exercise_data)

    session.add(new_exercise_log)
    session.commit()
    session.refresh(new_exercise_log)

    return new_exercise_log

@router.post("/set-logs/", response_model=SetLogRead)
def create_set_log(set_data: SetLogCreate,current_user: User = Depends(get_current_user),session: Session = Depends(get_session)):

    exercise_log = session.get(ExerciseLog, set_data.exercise_log_id)

    if not exercise_log:
        raise HTTPException(status_code=404, detail="Exercise log not found.")

    assert exercise_log.workout.check_in.user_id is not None
    if exercise_log.workout.check_in.user_id != current_user.id:
         raise HTTPException(status_code=403, detail="Not authorized to access this exercise log.")

    new_set_log = SetLog.model_validate(set_data)

    session.add(new_set_log)
    session.commit()
    session.refresh(new_set_log)

    return new_set_log

@router.get("/{workout_id}", response_model=WorkoutRead)
def get_single_workout(workout_id: int,current_user: User = Depends(get_current_user),session: Session = Depends(get_session)):
    workout = session.get(Workout, workout_id)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found.")

    assert workout.check_in.user_id is not None
    if workout.check_in.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this workout.")

    return workout

@router.get("/date/{check_in_date}", response_model=WorkoutRead)
def get_workout_from_date(check_in_date: str,current_user: User = Depends(get_current_user),session: Session = Depends(get_session)):

    query = (
        select(Workout)
        .join(CheckIn) 
        .where(CheckIn.check_in_date == check_in_date)
        .where(CheckIn.user_id == current_user.id)
    )
    workout = session.exec(query).first()

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found.")
    
    return workout


@router.delete("/exercise-logs/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise_log(exercise_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    exercise_log = session.get(ExerciseLog, exercise_id)
    
    if not exercise_log:
        raise HTTPException(status_code=404, detail="Exercise log not found.")

    
    try:
        owner_id = exercise_log.workout.check_in.user_id
    except AttributeError:
        raise HTTPException(status_code=404, detail="Related workout data not found.")

    if owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this exercise.")

    
    for set_log in exercise_log.set_logs:
        session.delete(set_log)

    session.delete(exercise_log)
    session.commit()
    
    return None

@router.delete("/set-logs/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_set_log( set_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    set_log = session.get(SetLog, set_id)
    
    if not set_log:
        raise HTTPException(status_code=404, detail="Set log not found.")

    try:
        owner_id = set_log.exercise_log.workout.check_in.user_id
    except AttributeError:
        raise HTTPException(status_code=404, detail="Related set data not found.")
        
    if owner_id != current_user.id:
         raise HTTPException(status_code=403, detail="Not authorized to delete this set.")

    session.delete(set_log)
    session.commit()
    
    return None

@router.patch('/set-logs/{set_id}', response_model=SetLogRead)
def update_set_log(set_id:int, set_update:SetLogUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    set_log = session.get(SetLog, set_id)
    if not set_log:
        raise HTTPException(status_code=404, detail="Set Log Not Found")
    
    try:
        owner_id = set_log.exercise_log.workout.check_in.user_id
    except AttributeError:
        raise HTTPException(status_code=404, detail="Related set data not found.")
        
    if owner_id != current_user.id:
         raise HTTPException(status_code=403, detail="Not authorized to delete this set.")
    
    update_data = set_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(set_log, key, value)

    session.add(set_log)
    session.commit()
    session.refresh(set_log)

    return set_log