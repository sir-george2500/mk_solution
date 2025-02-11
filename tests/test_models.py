import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.models import CreateUser, Base


# Database URL (use a test database or an in-memory SQLite database)
DATABASE_URL = "sqlite:///:memory:"

# Set up an in-memory SQLite database for testing
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database schema in the test database
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Creates a new database session for each test."""
    session = SessionLocal()
    yield session
    session.close()

def test_create_user(db_session):
    """Test creating a user."""
    # Create a new user
    new_user = CreateUser(
        name="John Doe",
        email="johndoe@example.com",
        phone="1234567890",
        role="Admin",
        profile_url="http://example.com/profile.jpg",
        address="123 Main St, Anytown",
        business_url="http://business.com"
    )
    db_session.add(new_user)
    db_session.commit()

    # Check if the user is added
    user = db_session.query(CreateUser).filter_by(email="johndoe@example.com").first()
    assert user is not None
    assert user.name == "John Doe"
    assert user.email == "johndoe@example.com"
    assert user.phone == "1234567890"
    assert user.role == "Admin"
    assert user.profile_url == "http://example.com/profile.jpg"
    assert user.address == "123 Main St, Anytown"
    assert user.business_url == "http://business.com"

def test_create_user_duplicate_email(db_session):
    """Test creating a user with a duplicate email."""
    # Create the first user
    user1 = CreateUser(
        name="Jane Doe",
        email="janedoe@example.com",
        phone="0987654321",
        role="User"
    )
    db_session.add(user1)
    db_session.commit()

    # Try creating a user with the same email
    user2 = CreateUser(
        name="John Smith",
        email="janedoe@example.com",  # Same email
        phone="1122334455",
        role="User"
    )
    
    # Ensure that an IntegrityError is raised due to the unique constraint on email
    with pytest.raises(IntegrityError):
        db_session.add(user2)
        db_session.commit()

def test_create_user_with_optional_fields(db_session):
    """Test creating a user with optional fields."""
    # Create a user with only required fields (name, email)
    user = CreateUser(
        name="Mark Smith",
        email="marksmith@example.com"
    )
    db_session.add(user)
    db_session.commit()

    # Check that the optional fields are null by default
    user = db_session.query(CreateUser).filter_by(email="marksmith@example.com").first()
    assert user is not None
    assert user.name == "Mark Smith"
    assert user.email == "marksmith@example.com"
    assert user.phone is None
    assert user.role is None
    assert user.profile_url is None
    assert user.address is None
    assert user.business_url is None

def test_create_user_timestamp_fields(db_session):
    """Test that created_at and updated_at are automatically populated."""
    # Create a user
    user = CreateUser(
        name="Alice Green",
        email="alicegreen@example.com"
    )
    db_session.add(user)
    db_session.commit()

    # Check the created_at and updated_at fields
    assert user.created_at is not None
    assert user.updated_at is not None
def test_update_user(db_session):
    """Test updating a user's information."""
    # Create a user
    user = CreateUser(
        name="Samuel Brown",
        email="samuelbrown@example.com"
    )
    db_session.add(user)
    db_session.commit()

    # Update the user's role
    user.role = "Manager"
    db_session.add(user)  # Mark the object as modified
    db_session.commit()

    # Fetch the updated user and check the role
    updated_user = db_session.query(CreateUser).filter_by(email="samuelbrown@example.com").first()
    assert updated_user.role == "Manager"

