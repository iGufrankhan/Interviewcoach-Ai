import random
from datetime import datetime, timedelta, timezone

def generate_otp(length: int = 6):

    otp = "".join([str(random.randint(0,9)) for _ in range(length)])

    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=5)

    return {
        "otp": otp,
        "expires_at": expiry_time
    }
    