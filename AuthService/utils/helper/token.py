import os
import datetime
from jose import jwt, JWTError

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


def create_access_token(user_id: str):
    if not SECRET_KEY:
        raise Exception("JWT_SECRET_KEY is not set")

    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_access_token(token: str):
    if not SECRET_KEY:
        raise Exception("JWT_SECRET_KEY is not set")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except JWTError:
        raise Exception("Invalid or expired token")
    
    
    
    
