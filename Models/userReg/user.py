from mongoengine import Document, StringField, DateTimeField, EmailField, BooleanField
from datetime import datetime


class User(Document):
    meta = {"collection": "users"}

    email = EmailField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    fullname = StringField()
    is_email_verified = BooleanField(default=False)
    
    created_at = DateTimeField(default=datetime.now)

