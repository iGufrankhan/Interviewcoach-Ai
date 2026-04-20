from AuthService.controllers.auth.emailSignup import (
    initializeemailsignup,
    verifyotp,
    complete_registration,
)
from AuthService.controllers.auth.login_service import login_user
from AuthService.controllers.auth.emailSignup import resend_otp
from AuthService.schemas.user import UserResponse
from  lib.helper.SetCookies import set_cookies
from AuthService.controllers.auth.logout import logout_user


async def SendOTP(email: str):
    return await initializeemailsignup(email)


async def VerifyOTP(email: str, otp: str):
    return await verifyotp(email, otp)


async def CompleteRegistration(email: str, password: str, fullname: str = "", registration_token: str = ""):
    registration_result= await complete_registration(
        email=email,
        password=password,
        fullname=fullname,
        registration_token=registration_token
    )
    if registration_result.access_token and registration_result.refresh_token:
        set_cookies([
            ("access_token", registration_result.access_token, {"httponly": True, "secure": True}),
            ("refresh_token", registration_result.refresh_token, {"httponly": True, "secure": True})
        ])
        
    return registration_result


async def LoginUser(email: str, password: str) -> UserResponse:
    login_result = await login_user(email, password)

    if(login_result.access_token and login_result.refresh_token):
        set_cookies([
            ("access_token", login_result.access_token, {"httponly": True, "secure": True}),
            ("refresh_token", login_result.refresh_token, {"httponly": True, "secure": True})
        ])
        
    return login_result
         
    
async def RefreshToken(refresh_token: str):
    return await login_user(refresh_token=refresh_token)


async def LogoutUser(refresh_token: str):
   
    logout_result = await logout_user(refresh_token)
    set_cookies([
        ("access_token", "", {"httponly": True, "secure": True, "max_age": 0}),
        ("refresh_token", "", {"httponly": True, "secure": True, "max_age": 0})
    ])
    
    return logout_result



async def ResendOTP(email: str):
    return await resend_otp(email)
