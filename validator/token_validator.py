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



async def validate_token(token: str):
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
