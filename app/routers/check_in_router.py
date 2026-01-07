from fastapi import APIRouter, Depends, HTTPException
from app.db.models.check_in_model import CheckIn
from app.db.models.user_model import User
from app.security import get_current_user
from sqlmodel import Session, select
from app.db.sqlite import get_session
from datetime import datetime
from zoneinfo import ZoneInfo  
from pydantic import BaseModel, field_validator


router = APIRouter(prefix='/checkins', tags=["checkins"])

class CheckInCreate(BaseModel):
    timezone: str 

    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        try:
            ZoneInfo(v)
            return v
        except Exception:
            raise ValueError("Invalid timezone string")

@router.post('/', response_model=CheckIn)
def create_check_in(check_in_data: CheckInCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    try: 
        user_timezone = ZoneInfo(check_in_data.timezone)
        user_date_now = datetime.now(user_timezone)
        today = user_date_now.date()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid timezone provided.")

    #checking for existing checked in entry for current day
    query = select(CheckIn).where(CheckIn.user_id == current_user.id, CheckIn.check_in_date == today)
    existing_check_in = session.exec(query).first()

    if existing_check_in:
        raise HTTPException(status_code=409, detail="Already checked in today.")
    
    check_in = CheckIn(check_in_date=today, user_id=current_user.id) # type: ignore
    try :
        session.add(check_in)
        session.commit()
        session.refresh(check_in)
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Failed To check In"
        )
    return check_in

@router.get("/", response_model=list[CheckIn])
def get_all_check_ins(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    query = select(CheckIn).where(CheckIn.user_id == current_user.id)
    check_ins = session.exec(query).all()
    return check_ins