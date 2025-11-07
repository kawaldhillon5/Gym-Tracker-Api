from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import UserCreate
from app.db.sqlite import get_session
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from app.db.models.user_model import User
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

router = APIRouter(prefix='/user')

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

print(get_password_hash("1234"))

@router.post('/')
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    print(user.password)
    new_user = User(user_name=user.user_name, email=user.email, hashed_password=get_password_hash(user.password))
    try :
        session.add(new_user)
        session.commit()
        session.refresh(new_user)         
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Username or email already exists."
        )
    return new_user
