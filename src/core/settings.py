import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Chift API"
    PROJECT_VERSION: str = "1.0.0"

    MONGO_URL: str = os.getenv("MONGO_URL")
    DB_NAME: str = os.getenv("DB_NAME")
    HOST: str = os.getenv("HOST")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE")
    PORT: int = os.getenv("PORT")


settings = Settings()
