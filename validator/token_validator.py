from fastapi import HTTPException, status
from dotenv import load_dotenv
import os
from jose import JWTError, jwt


# Load environment variables from .env file
load_dotenv()

token_secret = os.getenv("TOKEN_SECRET")
# Access environment variables
SECRET_KEY = os.getenv("SECRET_KEY", token_secret)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))



async def validate_user_token(token: str):
    """
    Validates a JWT token.

    Args:
        token (str): The JWT token string to validate.

    Raises:
        HTTPException: If the token is invalid or expired.

    Returns:
        dict: The payload of the decoded token if it is valid.
    """
    try:
        # Verify JWT token
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def validate_admin_token(token: str):
    """
    Validates a JWT token and checks if the user's role is Admin.

    Args:
        token (str): The JWT token string to validate.

    Raises:
        HTTPException: If the token is invalid, expired, or the user does not have Admin privileges.

    Returns:
        dict: The payload of the decoded token if the user has Admin privileges.
    """
    try:
        # Decode and verify the JWT token
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])

        # Get the user's role from the token payload
        role = payload.get("role")

        if role != "Admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied: Admin access required",
            )

        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

