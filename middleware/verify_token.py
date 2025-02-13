from fastapi import  Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from validator.token_validator import validate_token

security = HTTPBearer()
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
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
    await validate_token(token)
    return credentials
