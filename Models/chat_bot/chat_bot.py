from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class ChatSession(Document):
    """Store chat sessions for each user"""
    meta = {'collection': 'chat_sessions'}
    
    user_id = StringField(required=True)  # User's email
    email = StringField(required=True)
    title = StringField(default="New Chat")
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    

class ChatMessage(Document):
    """Store individual messages in a chat session"""
    meta = {'collection': 'chat_messages'}
    
    session_id = StringField(required=True)  # Reference to ChatSession
    role = StringField(required=True, choices=['user', 'assistant'])  # Who sent message
    content = StringField(required=True)  # The actual message
    timestamp = DateTimeField(default=datetime.now)