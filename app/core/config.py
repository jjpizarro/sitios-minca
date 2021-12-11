from pydantic import BaseSettings, EmailStr
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
   API_V1_STR: str = "/api/v1"
   PROJECT_NAME: str = "Sitios en minca"
 
   POSTGRES_SERVER: str = "localhost"
   POSTGRES_USER: str = "fastapi"
   POSTGRES_PASSWORD: str = "123123"
   POSTGRES_DB: str = "minca"
   SQLALCHEMY_DATABASE_URI: Optional[str] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

   # 60 minutes * 24 hours * 8 days = 8 days
   ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
   JWT_SECRET: str = "RFnq5vfS9XBUHbNjDSX3PRE8M2qQPRygJUfggZCDkYewYx69FzQqVnTV69k8TkYwm"
   ALGORITHM: str = "HS256"

   FIRST_SUPERUSER: EmailStr = "admin@ccsantamarta.com"
   FIRST_SUPERUSER_PW: str = "123123"

   class Config:
       case_sensitive = True

@lru_cache
def get_settigns():
    return Settings()

settings = get_settigns()