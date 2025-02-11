import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from typing import Any, Dict
from models.schemas.user_schemas import CreateUserSchema

@pytest.fixture
def valid_user_data() -> Dict[str, Any]:
    """Fixture for valid user data."""
    return {
        "name": "Alice Green",
        "email": "alicegreen@example.com",
        "phone": "+1234567890",
        "role": "Manager",
        "password": "securePassword123",
        "forget_password_token": None,
        "forget_password_token_expiry": None,
        "forget_password_token_used": False,
        "verify_user_token": None,
        "verify_user_token_expiry": None,
        "verify_user_token_used": False,
        "profile_url": "https://example.com/profile/alice-green",
        "address": "123 Elm Street, Springfield",
        "business_url": "https://alicegreenbusiness.com",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

class TestCreateUserSchema:
    def test_valid_user(self, valid_user_data):
        """Test creating a user with valid data."""
        user = CreateUserSchema(**valid_user_data)
        assert user.name == valid_user_data["name"]
        assert user.email == valid_user_data["email"]
        assert user.phone == valid_user_data["phone"]
        assert user.role == valid_user_data["role"]
        assert user.password == valid_user_data["password"]
        assert user.forget_password_token == valid_user_data["forget_password_token"]
        assert user.forget_password_token_expiry == valid_user_data["forget_password_token_expiry"]
        assert user.forget_password_token_used == valid_user_data["forget_password_token_used"]
        assert user.verify_user_token == valid_user_data["verify_user_token"]
        assert user.verify_user_token_expiry == valid_user_data["verify_user_token_expiry"]
        assert user.verify_user_token_used == valid_user_data["verify_user_token_used"]
        assert user.address == valid_user_data["address"]
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_minimal_user(self):
        """Test creating a user with minimal required fields."""
        minimal_data = {
            "name": "Bob Smith",
            "email": "bob@example.com",
            "phone": "+9876543210",
            "role": "User",
            "password": "password123"
        }
        user = CreateUserSchema(**minimal_data)
        assert user.name == minimal_data["name"]
        assert user.email == minimal_data["email"]
        assert user.phone == minimal_data["phone"]
        assert user.role == minimal_data["role"]
        assert user.password == minimal_data["password"]
        assert user.forget_password_token is None
        assert user.forget_password_token_expiry is None
        assert user.forget_password_token_used is False
        assert user.verify_user_token is None
        assert user.verify_user_token_expiry is None
        assert user.verify_user_token_used is False
        assert user.profile_url is None
        assert user.address is None
        assert user.business_url is None
        assert user.created_at is None
        assert user.updated_at is None

    def test_invalid_password(self, valid_user_data):
        """Test validation for invalid passwords."""
        invalid_passwords = ["short", "1234567", "pass"]
        for password in invalid_passwords:
            invalid_data = valid_user_data.copy()
            invalid_data["password"] = password
            with pytest.raises(ValidationError):
                CreateUserSchema(**invalid_data)

    def test_field_types(self, valid_user_data):
        """Ensure all fields are correctly typed."""
        user = CreateUserSchema(**valid_user_data)
        assert isinstance(user.name, str)
        assert isinstance(user.email, str)
        assert isinstance(user.phone, str)
        assert isinstance(user.role, str)
        assert isinstance(user.password, str)
        assert isinstance(user.forget_password_token, (str, type(None)))
        assert isinstance(user.forget_password_token_expiry, (datetime, type(None)))
        assert isinstance(user.forget_password_token_used, bool)
        assert isinstance(user.verify_user_token, (str, type(None)))
        assert isinstance(user.verify_user_token_expiry, (datetime, type(None)))
        assert isinstance(user.verify_user_token_used, bool)
        assert isinstance(user.address, (str, type(None)))
        assert isinstance(user.created_at, (datetime, type(None)))
        assert isinstance(user.updated_at, (datetime, type(None)))

