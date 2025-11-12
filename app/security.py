from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import timezone, datetime, timedelta
from jose import JWTError, jwt
from sqlmodel import Session, select
from app.db.models.user_model import User
from app.db.sqlite import get_session
from app.schemas.user_schema import TokenData
import os
from dotenv import load_dotenv

load_dotenv()



SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = os.getenv("ALGORITHM") 
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #type: ignore
    return encoded_jwt



async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #type: ignore

        username = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(user_name=username)

    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.user_name == token_data.user_name)).first()

    if user is None:
        raise credentials_exception

    return user