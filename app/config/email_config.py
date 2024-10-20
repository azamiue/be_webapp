from fastapi_mail import ConnectionConfig
from pydantic import EmailStr
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Get the current directory (config folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the app directory
app_dir = os.path.dirname(current_dir)
# Construct the path to the .env file
env_path = os.path.join(app_dir, '.env')

# Load the .env file
load_dotenv(env_path)

class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True

    class Config:
        env_file = env_path
        env_file_encoding = 'utf-8'
        extra = 'ignore'

email_settings = EmailSettings()

conf = ConnectionConfig(
    MAIL_USERNAME=email_settings.MAIL_USERNAME,
    MAIL_PASSWORD=email_settings.MAIL_PASSWORD,
    MAIL_FROM=email_settings.MAIL_FROM,
    MAIL_PORT=email_settings.MAIL_PORT,
    MAIL_SERVER=email_settings.MAIL_SERVER,
    MAIL_STARTTLS=email_settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=email_settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

print("Email configuration loaded:")
print(f"Username: {conf.MAIL_USERNAME}")
print(f"From: {conf.MAIL_FROM}")
print(f"Server: {conf.MAIL_SERVER}")
print(f"Port: {conf.MAIL_PORT}")
print(f"STARTTLS: {conf.MAIL_STARTTLS}")
print(f"SSL_TLS: {conf.MAIL_SSL_TLS}")