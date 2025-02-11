import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import CreateUser  # Assuming CreateUser is the model from models.py
from models.schemas.user_schemas import CreateUserSchema
from crud_engine.user_crud import UserCRUD

# Setting up a test database
DATABASE_URL = "sqlite:///:memory:"  # In-memory database for testing

# Create an engine and sessionmaker for the test
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database (for testing purposes)
CreateUser.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for each test."""
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="function")
def user_data():
    """Provide a sample user data to create a new user."""
    return CreateUserSchema(
        name="Alice Green",
        email="someuser@example.com",
        phone="+1234567890",
        role="Manager",
        password="password123"
    )

@pytest.fixture(scope="function")
def user_crud():
    """Provide an instance of the UserCRUD class."""
    return UserCRUD()

def test_create_user(db_session, user_data, user_crud):
    """Test the create_user method in UserCRUD."""
    
    # Check if the user already exists
    existing_user = user_crud.get_user_by_email(db_session, user_data.email)
    if existing_user:
        pytest.skip(f"User with email {user_data.email} already exists, skipping test.")

    # Create the user since it doesn't exist
    user = user_crud.create_user(db_session, user_data)

    # Ensure the user is created and has the expected attributes
    assert user.name == user_data.name
    assert user.email == user_data.email
    assert user.phone == user_data.phone
    assert user.role == user_data.role
    assert user.created_at is not None
    assert user.updated_at is not None

def test_get_user_by_email(db_session, user_data, user_crud):
    """Test the get_user_by_email method in UserCRUD."""
    
    # Directly fetch the user without recreating
    fetched_user = user_crud.get_user_by_email(db_session, user_data.email)

    # Ensure the user is found
    assert fetched_user is not None
    assert fetched_user.email == user_data.email
    assert fetched_user.name == user_data.name

def test_get_user_by_email_not_found(db_session, user_crud):
    """Test getting a user by email when the user does not exist."""
    non_existing_email = "nonexistinguser@example.com"
    fetched_user = user_crud.get_user_by_email(db_session, non_existing_email)

    # Ensure that no user is found
    assert fetched_user is None

