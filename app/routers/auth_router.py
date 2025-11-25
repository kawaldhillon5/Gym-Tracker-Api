from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserCreate,  UserRead, Token
from app.db.sqlite import get_session
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.db.models.user_model import User
from pwdlib import PasswordHash
from datetime import timedelta
from pydantic import BaseModel
from app.security import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
import re

password_hash = PasswordHash.recommended()

router = APIRouter(prefix='/user', tags=['Auth'])

class CheckPasswordResult(BaseModel):
    is_valid: bool
    message: str

def check_password_strenght(password: str) -> CheckPasswordResult:

    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
        
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")

    if not re.search(r"[0-9]", password):
        errors.append("Password must contain at least one number.")
        
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        errors.append("Password must contain at least one special character.")

    # If we have errors, return False and join the messages
    if errors:
        return CheckPasswordResult(
            is_valid=False, 
            message=" ".join(errors) # Joins all errors into one string
        )

    return CheckPasswordResult(is_valid=True, message="Password is strong.")

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_pass: str, hased_pass: str) -> bool:
    return password_hash.verify(plain_pass, hased_pass)

@router.post('/', response_model= UserRead )
def create_user( user: UserCreate, session: Session = Depends(get_session)):

    if (user.password != user.confirmPassword):
        raise HTTPException(
            status_code=400,
            detail= "Password and Confirm Password do not match"
        )
    
    pass_check_result = check_password_strenght(user.password)

    if not pass_check_result.is_valid:
        raise HTTPException(
            status_code=400,
            detail= pass_check_result.message
        ) 

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

@router.post('/login', response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user_from_db = session.exec(select(User).where(User.user_name == form_data.username)).first()
    if not user_from_db:
        raise HTTPException(
            status_code=404,
            detail= "User Not Found"
        )
    if verify_password(form_data.password, user_from_db.hashed_password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {"sub": user_from_db.user_name}
        access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
        return Token(access_token=access_token, token_type="bearer")
    
    else: 
        raise HTTPException(
            status_code = 401,
            detail= "Incorrect Password"
        )
    
@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user