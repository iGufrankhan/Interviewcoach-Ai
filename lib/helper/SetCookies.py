



async def set_cookies(response, access_token, refresh_token):
    """Set access and refresh tokens in HTTP-only cookies."""
    
    # Set access token cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # Set to True in production
        samesite="Strict",
        max_age=15 * 60  # 15 minutes
    )
    
    # Set refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # Set to True in production
        samesite="Strict",
        max_age=7 * 24 * 60 * 60  # 7 days
    )
    
    
    
async def clear_cookies(response):
    """Clear access and refresh token cookies."""
    
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
        
    