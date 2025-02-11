from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from config.db import db_connection
from crud_engine.user_crud import UserCRUD
from models.schemas.user_schemas import CreateUserSchema
from validator.user_validator import UserValidator
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from jose import jwt
import secrets

# Load environment variables from .env file
load_dotenv()

# Create an instance of the CRUD class
crud = UserCRUD()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_validator = UserValidator(crud=crud, pwd_context=pwd_context)

# Access environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
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
