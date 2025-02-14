from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from config.db import db_connection
from crud_engine.user_crud import UserCRUD  
import logging
from logic.auth.utils import generate_verification_code_alphanumeric
from validator.user_validator import UserValidator

crud = UserCRUD()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_validator = UserValidator(crud=crud, pwd_context=pwd_context)

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

        user = user_validator.validate_user_exists(session, user_id)
        
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

async def update_user_data(user_id: int, update_data: dict, session: Session):
    """
    Updates user data based on the provided user ID and update fields.

    Args:
        user_id (int): The ID of the user to update.
        update_data (dict): A dictionary containing the fields to update.
        session (Session): The database session.
        validator (UserValidator): An instance of UserValidator for validation.

    Returns:
        dict: The updated user data if the update is successful.

    Raises:
        HTTPException: If there's an error during the update.
    """
    try:
        # Validate if the user exists using UserValidator
        _ = user_validator.validate_user_exists(session, user_id)

        # Update the user with the provided data
        updated_user = UserCRUD.update_user(
            db=session,
            user_id=user_id,
            **update_data  # Unpack the update_data dictionary
        )

        # Create a dictionary with only the required fields for response
        updated_user_data = {
            "user_id": updated_user.id,
            "user_role": updated_user.role,
            "user_name": updated_user.name,
            "email": updated_user.email,
            "profile_picture": updated_user.profile_url,
            "business_url": updated_user.business_url,
            "is_verified": updated_user.is_email_verified,
        }

        # Return the updated user data
        return updated_user_data

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



def send_code_to_verify_email(email: str, session: Session = Depends(db_connection)):
    """
    Send a verification code to the user's email.

    Args:
        email (str): The user's email address.
        session (Session): The database session.

    Raises:
        HTTPException: If the user is not found.
    """
    # Generate a verification code
    code = generate_verification_code_alphanumeric()


    user = crud.get_user_by_email(session, email)

     # Validate if the user exists using UserValidator
    _ = user_validator.validate_user_exists(session, user.id)
    # Extract the user ID as an integer (not as a SQLAlchemy column)
    user_id = user.id

    # Ensure the user_id is valid
    if not isinstance(user_id, int):
        raise HTTPException(status_code=500, detail="Invalid user ID")

    # Update the user with the verification code
    update_data = {"verify_user_token": code}
    _ = crud.update_user(session, user_id=user_id, **update_data)

    # Return a success message
    return {"message": "Verification code sent successfully."}

