import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path('') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Chift API"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # Equal to 8 days
    DB_URL: str = os.getenv("DB_URL")
    DB_NAME: str = os.getenv("DB_NAME")
    HOST: str = os.getenv("HOST")
    PORT: int = os.getenv("PORT")
    CHIFT_URL: str = os.getenv("CHIFT_URL")
    CHIFT_DB: str = os.getenv("CHIFT_DB")
    CHIFT_USERNAME: str = os.getenv("CHIFT_USERNAME")
    CHIFT_PASSWORD: str = os.getenv("CHIFT_PASSWORD")


settings = Settings()
