# routes/api/v1/auth/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import db_connection
from logic.auth.register_and_login import login_user, register_new_user
from models.schemas.login_user_schema import LoginUserSchemas
from models.schemas.user_schemas import CreateUserSchema

auth_router = APIRouter()

# Dependency to get DB session
def get_db():
    db = db_connection()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/auth/register")
async def create_user(user_data: CreateUserSchema, session: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user_data (UserCreate): User data to create the user.
        session (Session): Database session.

    Returns:
        dict: Message indicating successful user creation.
    """
    try:
        await register_new_user(user_data, session)
        return {"message": "User created successfully"}
    except HTTPException as e:
        raise e


@auth_router.post("/auth/login")
async def login(user_data: LoginUserSchemas, session: Session = Depends(get_db)):
    """
    Login user with provided credentials.

    Args:
        user_data (UserLogin): User credentials for login.
        session (Session): Database session.

    Returns:
        dict: Response containing login details.
    """
    try:
        response = await login_user(user_data, session)  # Await the login_user function
        return response
    except HTTPException as e:
        raise e



