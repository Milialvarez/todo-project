from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "change-me-to-a-random-secret"  
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 
    EMAIL_FROM: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 465


    class Config:
        env_file = ".env"

settings = Settings()
DATABASE_URL = settings.DATABASE_URL