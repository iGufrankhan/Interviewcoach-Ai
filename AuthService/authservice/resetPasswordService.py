from AuthService.controllers.auth.resetPassword import (
    resend_password_reset_otp,
    reset_password,
    request_password_reset,
    verify_password_reset_otp
)



async def RequestPasswordReset(email: str):
    return await request_password_reset(email)

async def VerifyPasswordResetOTP(email: str, otp: str):
    return await verify_password_reset_otp(email, otp)

async def ResendPasswordResetOTP(email: str):
    return await resend_password_reset_otp(email)

async def ResetPassword(email: str, new_password: str):
    return await reset_password(email, new_password)