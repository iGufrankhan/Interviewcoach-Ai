
import os

from fastapi_mail import ConnectionConfig

MY_EMAIL = os.getenv("GMAIL_USER")
MY_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")



CreateTransporter= ConnectionConfig(
    MAIL_USERNAME=MY_EMAIL,
    MAIL_PASSWORD=MY_APP_PASSWORD,
    MAIL_FROM=MY_EMAIL,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="InterviewCoach AI",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)