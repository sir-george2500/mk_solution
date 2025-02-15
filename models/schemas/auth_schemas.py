from pydantic import BaseModel, EmailStr, Field, ConfigDict

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
