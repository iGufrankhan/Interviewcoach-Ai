from mongoengine import Document, StringField, DateTimeField
from datetime import datetime


class User(Document):
    meta = {'collection': 'users'}

    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    name = StringField()
    created_at = DateTimeField(default=datetime.now)
    
    