## send otp, verify otp, complete registration, login user

from AuthService.utils.emailservice.emailSignup import (
    initializeemailsignup,
    login_user,
    verifyotp,
    complete_registration,
)


async def SendOTP(email: str):
    return await initializeemailsignup(email)


async def VerifyOTP(email: str, otp: str):
    return await verifyotp(email, otp)


async def CompleteRegistration(email: str, user_data: dict):
    return await complete_registration(
        email=email,
        password=user_data["password"],
        name=user_data.get("name", ""),
    )


async def LoginUser(email: str, password: str):
    return await login_user(email, password)
