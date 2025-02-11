import pytest
from datetime import datetime
from pydantic import ValidationError, EmailStr, HttpUrl
from typing import Any, Dict

from models.schemas.user_schemas import CreateUserSchema

@pytest.fixture
def valid_user_data() -> Dict[str, Any]:
    return {
        "name": "Alice Green",
        "email": "alicegreen@example.com",
        "phone": "+1234567890",
        "role": "Manager",
        "profile_url": "https://example.com/profile/alice-green",
        "address": "123 Elm Street, Springfield",
        "business_url": "https://alicegreenbusiness.com"
    }

class TestCreateUserSchema:
    def test_valid_full_user(self, valid_user_data):
        """Test creating a user with all fields populated."""
        user = CreateUserSchema(**valid_user_data)
        assert user.name == valid_user_data["name"]
        assert user.email == valid_user_data["email"]
        assert user.phone == valid_user_data["phone"]
        # Normalize URLs by removing trailing slashes for comparison
        if user.profile_url:
            assert str(user.profile_url).rstrip('/') == valid_user_data["profile_url"].rstrip('/')
        if user.business_url:
            assert str(user.business_url).rstrip('/') == valid_user_data["business_url"].rstrip('/')

    def test_minimal_valid_user(self):
        """Test creating a user with only required fields."""
        minimal_data = {
            "name": "Bob Smith",
            "email": "bob@example.com"
        }
        user = CreateUserSchema(**minimal_data)
        assert user.name == minimal_data["name"]
        assert user.email == minimal_data["email"]
        assert user.phone is None
        assert user.role is None
        assert user.profile_url is None
        assert user.address is None
        assert user.business_url is None

    def test_invalid_email(self, valid_user_data):
        """Test that invalid email addresses are rejected."""
        invalid_emails = [
            "notanemail",
            "missing@domain",
            "@nodomain.com",
            "spaces in@email.com"
        ]
        
        for invalid_email in invalid_emails:
            invalid_data = valid_user_data.copy()
            invalid_data["email"] = invalid_email
            with pytest.raises(ValidationError):
                CreateUserSchema(**invalid_data)

    def test_none_optional_fields(self, valid_user_data):
        """Test that None is accepted for optional fields."""
        optional_fields = [
            "phone", "role", "profile_url", "address", "business_url"
        ]
        
        for field in optional_fields:
            modified_data = valid_user_data.copy()
            modified_data[field] = None
            user = CreateUserSchema(**modified_data)
            assert getattr(user, field) is None

    def test_field_types(self, valid_user_data):
        """Test that fields are converted to correct types."""
        user = CreateUserSchema(**valid_user_data)
        assert isinstance(user.name, str)
        assert isinstance(user.email, str)
        assert isinstance(user.phone, str)
        assert isinstance(user.role, str)
        assert isinstance(user.profile_url, HttpUrl) or user.profile_url is None
        assert isinstance(user.address, str) or user.address is None
        assert isinstance(user.business_url, HttpUrl) or user.business_url is None
