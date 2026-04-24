from mongoengine import ReferenceField, StringField, ListField, DateTimeField
from datetime import datetime
from utils.async_model import AsyncDocument
from Models.userReg.user import User

class Resume_data(AsyncDocument):
    meta = {'collection': 'resume_data'}
    user = ReferenceField(User, required=True)
    name = StringField(required=True)
    skills = ListField(StringField())
    experience = ListField(StringField())
    education = ListField(StringField())
    projects = ListField(StringField())
    created_at = DateTimeField(default=datetime.now)


