# routes/api/v1/auth/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import db_connection
from logic.auth.auth_logic import login_user, register_new_user, send_code_to_verify_email
from models.schemas.login_user_schema import LoginUserSchemas
from models.schemas.user_schemas import CreateUserSchema
from fastapi import status
from fastapi_mail import MessageSchema
from config.email import fastmail
from datetime import datetime, timezone
from crud_engine.user_crud import crud 
from models.schemas.auth_schemas import VerifyEmailRequest
from models.schemas.auth_schemas import BusinessCertificateUpload 
from models.schemas.auth_schemas import BusinessCertificateReview
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
        response = await register_new_user(user_data, session)
        return response
    except HTTPException as e:
        raise e
    
@auth_router.post("/auth/verify-email", 
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Email verified successfully"},
        400: {"description": "Invalid or expired verification code"},
        404: {"description": "User not found"}
    }
)
async def verify_email(
    verify_data: VerifyEmailRequest,
    session: Session = Depends(get_db)
):
    try:
        user = crud.get_user_by_email(session, verify_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if code is expired
        if datetime.now(timezone.utc) > user.verify_user_token_expiry:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired"
            )

        # Verify code
        if user.verify_user_token != verify_data.code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification code"
            )

        # Update user verification status
        crud.update_user(
            session,
            user.id,
            is_email_verified=True,
            verify_user_token=None,
            verify_user_token_expiry=None,
            verify_user_token_used=True
        )

        return {"message": "Email verified successfully"}

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

@auth_router.post("/auth/send-verify-email-code")
async def send_verify_email_code(email:str, session:Session = Depends(get_db)):
    """
    Send a verification code to the user's email.

    Args:
        email (str): The user's email address.
    """
    try:
        await send_code_to_verify_email(email, session)
        return {"message": "Verification code sent successfully"}
    except HTTPException as e:
        raise e
    
@auth_router.put("/auth/upload-business-certificate/{user_id}", 
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Business certificate uploaded successfully"},
        404: {"description": "User not found"},
        400: {"description": "Email not verified"}
    }
)
async def upload_business_certificate(
    user_id: int,
    certificate_data: BusinessCertificateUpload,
    session: Session = Depends(get_db)
):
    try:
        user = crud.get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please verify your email first"
            )

        # Update user with certificate URL and set onboarding status
        crud.update_user(
            session,
            user_id,
            business_url=certificate_data.certificate_url,
            is_onboarded=True,
            is_approved=False  # Reset approval status if certificate is reuploaded
        )

        return {"message": "Business certificate uploaded successfully"}
    except HTTPException as e:
        raise e



@auth_router.get("/auth/admin/onboarded-clients",
    responses={
        200: {"description": "List of onboarded clients retrieved successfully"},
        403: {"description": "Not authorized"}
    }
)
async def get_onboarded_clients(
    session: Session = Depends(get_db)
):
    try:
        clients = crud.get_onboarded_clients(session)
        return {
            "clients": [
                {
                    "user_id": client.id,
                    "name": client.name,
                    "email": client.email,
                    "business_url": client.business_url,
                    "onboarded_at": client.updated_at
                }
                for client in clients
            ]
        }
    except HTTPException as e:
        raise e

@auth_router.post("/auth/admin/review-business-certificate",
    responses={
        200: {"description": "Business certificate review completed"},
        404: {"description": "User not found"},
        403: {"description": "Not authorized"}
    }
)
async def review_business_certificate(
    review_data: BusinessCertificateReview,
    session: Session = Depends(get_db)
):
    try:
        user = crud.get_user_by_id(session, review_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update approval status
        crud.update_user(
            session,
            review_data.user_id,
            is_approved=review_data.approved,
            is_onboarded=review_data.approved  # Set to false if rejected
        )

        # Send email notification
        message = MessageSchema(
            subject="Business Certificate Review Update",
            recipients=[user.email],
            template_body={
                "name": user.name,
                "status": "approved" if review_data.approved else "rejected",
                "reason": review_data.reason if not review_data.approved else None
            },
            subtype="html"
        )

        await fastmail.send_message(
            message, 
            template_name="certificate_review.html"
        )

        return {"message": f"Business certificate {review_data.approved and 'approved' or 'rejected'}"}
    except HTTPException as e:
        raise e
