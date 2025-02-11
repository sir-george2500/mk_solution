from pydantic import BaseModel, EmailStr, HttpUrl, Field, ConfigDict
from typing import Optional
from datetime import datetime

class CreateUserSchema(BaseModel):
    name: str = Field(...,min_length=3, description="The full name of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    phone: Optional[str] = Field(None, description="The phone number of the user")
    role: Optional[str] = Field(None, description="The role of the user")
    profile_url: Optional[str] = Field(None, description="The profile picture URL of the user")  # Changed back to HttpUrl
    address: Optional[str] = Field(None, description="The address of the user")
    business_url: Optional[str] = Field(None, description="The business URL of the user")  # Changed back to HttpUrl
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Alice Green",
                "email": "alicegreen@example.com",
                "phone": "+1234567890",
                "role": "Manager",
                "profile_url": "https://example.com/profile/alice-green",
                "address": "123 Elm Street, Springfield",
                "business_url": "https://alicegreenbusiness.com"
            }
        }
    )
