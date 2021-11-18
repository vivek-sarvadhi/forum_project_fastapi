from pydantic import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig


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


conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = os.getenv("MAIL_PORT"),
    MAIL_SERVER = os.getenv("MAIL_SERVER"),
    MAIL_TLS = True,
    MAIL_SSL = False,
    TEMPLATE_FOLDER = Path(__file__).parent / 'templates',
)

setting = Settings()
