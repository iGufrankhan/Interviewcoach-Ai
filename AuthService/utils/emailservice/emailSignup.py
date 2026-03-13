


import datetime
import email

from AuthService.utils.emailservice.sendotp import send_otp_email
from AuthService.utils.helper.token import create_access_token
from utils.apierror import APIError
from Models.userReg.user.model import User
from utils.apiresponse import success_response, error_response


async def initializeemailsignup(email: str):
    
     user= User.objects(email=email).first()
     if user:
        raise APIError("Email already registered", "This email is already associated with an account.")
    
     msg= await send_otp_email(email, purpose="registration")
     
     if msg.get("status") != "success":
        raise APIError("Failed to send OTP", msg.get("message", "Unknown error occurred while sending OTP."))
    
     return email
 
 
 
 
async def verifyotp(email: str, otp: str):
    
    otp_entry = OTP.objects(email=email, purpose="registration").first()
    
    if not otp_entry:
        raise APIError("OTP not found", "No OTP found for this email. Please request a new one.")
    
    if otp_entry.expires_at < datetime.utcnow():
        otp_entry.delete()  # Clean up expired OTP
        raise APIError("OTP expired", "The OTP has expired. Please request a new one.")
    
    if otp_entry.otp != otp:
        raise APIError("Invalid OTP", "The provided OTP is incorrect. Please try again.")
    
    # OTP is valid, proceed with registration
    otp_entry.delete()  # Clean up used OTP
    return success_response("OTP verified successfully. You can now complete your registration.")  


async def complete_registration(email: str, password: str, name: str = ""):
    existing_user = User.objects(email=email).first()
    if existing_user:
        raise APIError("Email already registered", "This email is already associated with an account.")
    
    # Hash the password before storing (use a proper hashing algorithm in production)
    password_hash = hash(password)
    
    new_user = User(email=email, password_hash=password_hash, name=name)
    new_user.save()
    access_token = create_access_token(user_id=new_user.id)
    
    return success_response("Registration completed successfully", {"access_token": access_token, "token_type": "bearer"})




async  def login_user(email: str, password: str):
    user = User.objects(email=email).first()
    if not user:
        raise APIError("User not found", "No account found with this email.")
    
    # Verify password (use a proper hashing algorithm in production)
    if user.password_hash != hash(password):
        raise APIError("Invalid credentials", "The email or password is incorrect.")
    
    return success_response("Login successful. Welcome back!")
    
          
    
    
    
    
    
    
    
    
    