from AuthService.utils.emailservice.emailSignup import (
    initializeemailsignup,
    login_user,
    verifyotp,
    complete_registration,
)



async def SendOTP(email: str):
    return await initializeemailsignup(email)


async def VerifyOTP(email: str, otp: str, purpose: str = "registration"):
    return await verifyotp(email, otp, purpose)


async def CompleteRegistration(token: str, email: str, password: str, name: str = "", username: str = ""):
    return await complete_registration(token=token, email=email, password=password, name=name, username=username)


async def LoginUser(email: str, password: str):
    return await login_user(email, password)
