from mongoengine import Document, ReferenceField, StringField, ListField, DateTimeField
from datetime import datetime

from Models.userReg.user import User

class Resume_data(Document):
    meta = {'collection': 'resume_data'}
    user = ReferenceField(User, required=True)
    name = StringField(required=True)
    skills = ListField(StringField())
    experience = ListField(StringField())
    education = ListField(StringField())
    projects = ListField(StringField())
    created_at = DateTimeField(default=datetime.now)


