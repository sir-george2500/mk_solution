from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from crud_engine.user_crud import UserCRUD
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

async def get_user_data_by_id(user_id: int, session: Session):
    """
    Retrieves user data based on the provided user ID.

    Args:
        user_id (int): The ID of the user to retrieve data for.
        session (Session): The database session.

    Returns:
        dict: The user data if the user exists.

    Raises:
        HTTPException: If there's an error retrieving the user data.
    """
    try:
        crud = UserCRUD()

        # Retrieve the user data from the database using the provided user ID
        user = crud.get_user_by_id(session, user_id)  # If async, add `await`

        # Handle case where user is not found
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        # Create a dictionary with only the required fields
        user_data = {
            "user_id": user.id,
            "user_role": user.role,
            "user_name": user.name,
            "email": user.email,
            "profile_picture": user.profile_url,
            "business_url": user.business_url,
            "is_verified": user.is_email_verified,
        }

        # Return the user data
        return user_data

    except HTTPException as e:
        # Log and re-raise HTTPException if it occurs during validation
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as ex:
        # Log unexpected exceptions for debugging
        logger.error(f"Unexpected error: {ex}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

