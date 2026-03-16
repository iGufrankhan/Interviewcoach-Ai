from AuthService.controllers.emailservice.emailSignup import (
    initializeemailsignup,
    verifyotp,
    complete_registration,
)
from AuthService.controllers.emailservice.login_service import login_user


async def SendOTP(email: str):
    return await initializeemailsignup(email)


async def VerifyOTP(email: str, otp: str):
    return await verifyotp(email, otp)


async def CompleteRegistration(email: str, password: str, fullname: str = "", registration_token: str = ""):
    return await complete_registration(
        email=email,
        password=password,
        fullname=fullname,
        registration_token=registration_token
    )


async def LoginUser(email: str, password: str):
    return await login_user(email, password)
