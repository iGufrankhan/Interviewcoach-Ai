
import uuid
import random
import string
from Models.userReg.user import User


def generate_username(email: str) -> str:
    """Generate username from email."""
    base_username = email.split("@")[0]
    unique_id = str(uuid.uuid4())[:4]
    generated_username = f"{base_username}_{unique_id}"
    return generated_username


def generate_unique_username(email: str, full_name: str = ""):
    """Generate a unique username from email and optional full name."""
    if full_name:
        base_username = full_name.split()[0].lower()[:8]
    else:
        base_username = email.split("@")[0][:8]
    
    # Add random suffix to ensure uniqueness
    suffix = "".join(random.choices(string.digits, k=4))
    username = f"{base_username}_{suffix}"
    
    # Check if username exists
    while User.objects(username=username).first():
        suffix = "".join(random.choices(string.digits, k=4))
        username = f"{base_username}_{suffix}"
    
    return username