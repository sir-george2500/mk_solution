from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import db_connection
from middleware.verify_token import verify_user_token
from logic.users.users_logic import update_user_data,get_user_data_by_id

# Creating an APIRouter instance
user_data_router = APIRouter()

# Endpoint to get user profile
@user_data_router.get("/user/data/{user_id}", dependencies=[Depends(verify_user_token)])
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
        response = await get_user_data_by_id(user_id, session)
        return response
    except HTTPException as e:
        raise e

# Endpoint to update user data
@user_data_router.put("/user/data/{user_id}", dependencies=[Depends(verify_user_token)])
async def update_user_profile(user_id: int, update_data: dict, session: Session = Depends(db_connection)):
    """
    Update user profile data based on the provided user ID and data.

    Args:
        user_id (int): The ID of the user.
        update_data (dict): The data to update.
        session (Session): Database session.

    Returns:
        dict: Updated user profile data.
    """
    try:
        # Call the update_user_data function to handle the update logic
        updated_user_data = await update_user_data(user_id, update_data, session)
        return updated_user_data
    except HTTPException as e:
        raise e
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )

