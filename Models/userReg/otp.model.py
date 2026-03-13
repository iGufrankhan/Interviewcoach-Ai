from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class OTP(Document):
    meta = {'collection': 'otp_storage'}

    email = StringField(required=True)
    otp = StringField(required=True)
    purpose = StringField(required=True, default="registration")
    expires_at = DateTimeField(required=True)  # auto delete after expiry
    created_at = DateTimeField(default=datetime.now)