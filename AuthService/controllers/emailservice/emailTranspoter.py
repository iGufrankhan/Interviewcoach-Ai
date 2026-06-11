
from fastapi_mail import ConnectionConfig
from utils.constant import GMAIL_USER, GMAIL_APP_PASSWORD

MY_EMAIL = GMAIL_USER
MY_APP_PASSWORD = GMAIL_APP_PASSWORD



CreateTransporter= ConnectionConfig(
    MAIL_USERNAME=MY_EMAIL,
    MAIL_PASSWORD=MY_APP_PASSWORD,
    MAIL_FROM=MY_EMAIL,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="InterviewCoach AI",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)