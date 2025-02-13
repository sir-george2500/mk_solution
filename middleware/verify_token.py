from fastapi import  Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from validator.token_validator import validate_user_token , validate_admin_token

security = HTTPBearer()
async def verify_user_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Middleware function to verify the provided token using HTTP Bearer authentication.

    Args:
        credentials (HTTPAuthorizationCredentials): Credentials provided by the client, containing the token.

    Returns:
        str: The validated token if verification is successful.

    Raises:
        HTTPException: If the token is invalid or missing.
    """
    token = credentials.credentials
    await validate_user_token(token)
    return credentials

async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Middleware function to verify the provided token and check if the user's role is Admin.

    Args:
        credentials (HTTPAuthorizationCredentials): Credentials provided by the client, containing the token.

    Returns:
        str: The validated token if verification is successful and the user has Admin privileges.

    Raises:
        HTTPException: If the token is invalid, missing, or the user does not have Admin privileges.
    """
    token = credentials.credentials
    await validate_admin_token(token)
    return credentials

