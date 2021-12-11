from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

from app.core.security import get_password_hash
from app.core.security import verify_password

def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create(db: Session, obj_in: UserCreate) -> User:
    create_data = obj_in.dict() 
    create_data.pop("password")
    db_obj = User(**create_data) 
    db_obj.hashed_password = get_password_hash(obj_in.password)
    db.add(db_obj)
    db.commit()
    return db_obj

def is_superuser(user: User) -> bool:
        return user.is_superuser

def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

