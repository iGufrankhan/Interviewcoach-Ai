import jwt
import datetime
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def create_access_token(user_id: str):
    # Implement JWT token creation logic here
    # For simplicity, we'll return a dummy token. In production, use a library like PyJWT.\
    return jwt.encode({"user_id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")



def verify_access_token(token: str):
    # Implement JWT token verification logic here
    # For simplicity, we'll return a dummy user_id. In production, use a library like PyJWT.
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    
    
    
