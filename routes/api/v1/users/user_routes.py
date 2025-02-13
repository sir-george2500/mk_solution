from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import db_connection
from logic.users.users_logic import get_user_data_by_id
from middleware.verify_token import verify_token

# Creating an APIRouter instance
user_data_router = APIRouter()

# Endpoint to get user profile
@user_data_router.get("/user/data/{user_id}", dependencies=[Depends(verify_token)])
async def get_user_profile(user_id: int, session: Session = Depends(db_connection)):
    """
    Get user profile data based on the provided user ID and token.

    Args:
        user_id (int): The ID of the user.
        session (Session): Database session.

    Returns:
        dict: User profile data.
    """
    try:
        # Ensure get_user_data_by_id is compatible with async if being awaited
        response = await get_user_data_by_id(user_id, session)
        return response
    except HTTPException as e:
        raise e

