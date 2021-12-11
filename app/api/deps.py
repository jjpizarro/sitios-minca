from typing import Generator, Optional
from sqlalchemy.orm import Session
from app.database.session import SessionLocal

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from app.core.security import oauth2_scheme
from app.core.config import settings
from app.models.user import User

from app.schemas.token import TokenData

def get_db() -> Generator:
   try:
       db = SessionLocal()
       yield db
   finally:
       db.close()



async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user