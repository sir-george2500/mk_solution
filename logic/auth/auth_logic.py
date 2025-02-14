from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from config.db import db_connection
from crud_engine.user_crud import UserCRUD
from logic.auth.utils import generate_verification_code_alphanumeric
from models.schemas.login_user_schema import LoginUserSchemas
from models.schemas.user_schemas import CreateUserSchema
from validator.user_validator import UserValidator
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from jose import jwt

# Load environment variables from .env file
load_dotenv()

# Create an instance of the CRUD class
crud = UserCRUD()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_validator = UserValidator(crud=crud, pwd_context=pwd_context)
token_secret = os.getenv("TOKEN_SECRET")
# Access environment variables
SECRET_KEY = os.getenv("SECRET_KEY", token_secret)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

async def register_new_user(user_data: CreateUserSchema, session: Session = Depends(db_connection)):
    """
    Register a new user, handling validation, password hashing, and database operations.

    Args:
        user_data (UserCreate): User creation data.
        session (Session): The database session.

    Raises:
        HTTPException: If validation, password hashing, or user creation fails.
    """
    try:
        # Validate user data for duplication using the UserValidator
        user_validator.validate_for_duplicate_user(session, email=user_data.email)

        # Hash the user's password using the UserValidator
        hashed_password = pwd_context.hash(user_data.password)
        # Update the user_data with the hashed password
        user_data.password = hashed_password

        # Use the create_user method from the CRUD class
        crud.create_user(session, user_data)
    except HTTPException as e:
        # If an HTTPException occurs during validation, password hashing, or user creation, re-raise it
        raise e

def create_access_token(data: dict, role: str):
    """
    Create an access token with user data and role.

    Args:
        data (dict): User-specific data to encode in the token.
        role (str): User role to include in the token.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta

    # Add expiration and role to the payload
    to_encode.update({"exp": expire, "role": role})
    
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt



async def login_user(user_data: LoginUserSchemas, session: Session = Depends(db_connection)):
    """
    Login a user, validate credentials, and create an access token.

    Args:
        user_data (UserLogin): User login credentials.
        session (Session): The database session.

    Returns:
        dict: A dictionary containing the access token.
    """
    try:
        # Validate user credentials
        user = user_validator.validate_user_credentials(session, email=user_data.email, password=user_data.password)

        # Create an access token with the user's email and role
        access_token = create_access_token(data={"sub": user.email}, role=str(user.role))
        
        # Return login details including access token, user ID, email, user role, and email verification status
        return {
            "token_type": "bearer",
            "access_token": access_token,
            "user_id": user.id,
            "email": user.email,
            "user_role": user.role,
            "is_email_verified": user.is_email_verified
        }
    except HTTPException as e:
        # If an HTTPException occurs during validation or login, re-raise it
        raise e

async def send_code_to_verify_email(email:str, session:Session = Depends(db_connection)):
    """
    Send a verification code to the user's email.

    Args:
        email (str): The user's email address.
        code (str): The verification code to send.
    """
    # Implement email sending logic here
    code = generate_verification_code_alphanumeric()
    user = crud.get_user_by_email(session,email)

    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=5)
    

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    # store the user token in the database
    _= crud.update_user(session, user.id,
                        verify_user_token=code,
                        verify_user_token_expiry=expiry_time)

    # Mock email sending
    print(f"Verification code for {email}: {code}")





