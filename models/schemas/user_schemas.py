from pydantic import BaseModel, EmailStr, HttpUrl, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CreateUserSchema(BaseModel):
    name: str = Field(..., min_length=3, description="The full name of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    phone: str = Field(..., description="The phone number of the user")
    role: str = Field(..., description="The role of the user")
    password: str = Field(...,min_length=8, description="The password of the user")
    forget_password_token: Optional[str] = Field(None, description="Token for password reset")
    forget_password_token_expiry: Optional[datetime] = Field(None, description="Expiry time for the password reset token")
    forget_password_token_used: Optional[bool] = Field(False, description="Whether the password reset token has been used")
    verify_user_token: Optional[str] = Field(None, description="Token for user verification")
    verify_user_token_expiry: Optional[datetime] = Field(None, description="Expiry time for the user verification token")
    verify_user_token_used: Optional[bool] = Field(False, description="Whether the user verification token has been used")
    profile_url: Optional[str] = Field(None, description="The profile picture URL of the user")
    address: Optional[str] = Field(None, description="The address of the user")
    business_url: Optional[str] = Field(None, description="The business URL of the user")
    created_at: Optional[datetime] = Field(None, description="The time when the user was created")
    updated_at: Optional[datetime] = Field(None, description="The last time when the user was updated")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Alice Green",
                "email": "alicegreen@example.com",
                "phone": "+1234567890",
                "role": "Manager",
                "password": "password123",
                "forget_password_token": None,
                "forget_password_token_expiry": None,
                "forget_password_token_used": False,
                "verify_user_token": None,
                "verify_user_token_expiry": None,
                "verify_user_token_used": False,
                "profile_url": "https://example.com/profile/alice-green",
                "address": "123 Elm Street, Springfield",
                "business_url": "https://alicegreenbusiness.com",
                "created_at": "2023-12-01T12:00:00",
                "updated_at": "2023-12-01T12:00:00"
            }
        }
    )

