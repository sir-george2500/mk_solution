from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class VerifyEmailRequest(BaseModel):
    email: EmailStr = Field(..., description="Email address to verify")
    code: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "code": "123456"
            }
        }
    )

class BusinessCertificateUpload(BaseModel):
    certificate_url: str = Field(..., description="URL of the uploaded business certificate")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "certificate_url": "https://cloudinary.com/certificates/business123.pdf"
            }
        }
    )

class BusinessCertificateReview(BaseModel):
    user_id: int = Field(..., description="ID of the user whose certificate is being reviewed")
    approved: bool = Field(..., description="Whether the certificate is approved or rejected")
    reason: Optional[str] = Field(None, description="Reason for rejection if certificate is rejected")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "user_id": 1,
                "approved": False,
                "reason": "Certificate is not clearly legible"
            }
        }
    )