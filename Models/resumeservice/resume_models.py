from mongoengine import Document, StringField, ListField, DateTimeField
from datetime import datetime

class Resume_data(Document):
    meta = {'collection': 'resume_data'}

    name = StringField(required=True)
    skills = ListField(StringField())
    experience = ListField(StringField())
    education = ListField(StringField())
    projects = ListField(StringField())
    created_at = DateTimeField(default=datetime.now)


