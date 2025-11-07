from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserCreate
from app.db.sqlite import get_session
from sqlmodel import Session
router = APIRouter(prefix='/user')

@router.post('/')
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    print("User data from request:", user)
    return {"message": "User received", "username": user.user_name}