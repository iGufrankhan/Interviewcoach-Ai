from Models.userReg.user import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(email: str, password: str, name: str = None):
    password_hash = pwd_context.hash(password)
    user = User(email=email, password_hash=password_hash, name=name)
    user.save()
    return user
