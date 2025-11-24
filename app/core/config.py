import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520

    API_V1_STR: str = "/api/v1"
    SECRET_KEY = os.getenv("SECRET_KEY")
    PROJECT_NAME = os.getenv("PROJECT_NAME")

    # database posgres for production
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    DATABASE_URL = os.getenv("DATABASE_URL")
    DB_DEBUG_MODE: bool = os.getenv("DB_DEBUG_MODE").lower() in ("1", "true", "yes")

    # use sqlite for testing
    SQLITE_DATABASE_URL = os.getenv("SQLITE_DATABASE_URL")
    USE_SQLITE = os.getenv("USE_SQLITE").lower() in ("1", "true", "yes")

    # backend origin
    BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", "").split(",")

    # admin login
    FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")

    class Config:
        env_file = ".env"


settings = Settings()
