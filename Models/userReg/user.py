from mongoengine import StringField, DateTimeField, EmailField, BooleanField
from datetime import datetime
from utils.async_model import AsyncDocument


class User(AsyncDocument):
    meta = {"collection": "users"}

    email = EmailField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    fullname = StringField()
    is_email_verified = BooleanField(default=False)
    RefreshToken = StringField()
    created_at = DateTimeField(default=datetime.now)

