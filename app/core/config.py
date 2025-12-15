import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None
    SECRET_KEY: str = "change-me-to-a-random-secret"  
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 

    class Config:
        env_file = ".env"

settings = Settings()

DATABASE_URL = (
    settings.TEST_DATABASE_URL
    if os.getenv("PYTEST_CURRENT_TEST")
    else settings.DATABASE_URL
)