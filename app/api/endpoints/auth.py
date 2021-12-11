from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.crud import crud_user as crud
from app.schemas.user import UserCreate, User
from app.api import deps
from app.core.security import (
    
    create_access_token,
)
from app.crud.crud_user import authenticate
from app.models.user import User as UserModel

router = APIRouter()


@router.post("/login")
def login(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user


@router.post("/signup", response_model=User, status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """

    user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = crud.create(db=db, obj_in=user_in)

    return user