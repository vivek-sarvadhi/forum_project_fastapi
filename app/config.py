from pydantic import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    database_hostname: str = os.getenv("DATABASE_HOSTNAME")
    database_port: str = os.getenv("DATABASE_PORT")
    database_name: str = os.getenv("DATABASE_NAME")
    database_username: str = os.getenv("DATABASE_USERNAME")
    database_password: str = os.getenv("DATABASE_PASSWORD")
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minute: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    databse_url = f'postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}'

setting = Settings()
