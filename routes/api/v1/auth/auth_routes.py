from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import db_connection
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.config import Config

from logic.auth.register_and_login import register_new_user
from models.schemas.user_schemas import CreateUserSchema

auth_router = APIRouter()



def get_db():
    db = db_connection()
    try:
        yield db
    finally:
        db.close()


@auth_router.post("/user/register")
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
