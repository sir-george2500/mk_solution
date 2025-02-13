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



def test_get_user_by_id(db_session, user_crud):
    """Test the get_user_by_id method in UserCRUD."""

    # Correct the dictionary syntax
    user_create_data = CreateUserSchema(
        name="Alice Green",
        email="someuser9000@example.com",
        phone="+1234567890",
        role="Manager",
        password="password123"
    )

    # Create a user first
    created_user = user_crud.create_user(db_session, user_create_data)

    # Fetch the user by ID
    fetched_user = user_crud.get_user_by_id(db_session, created_user.id)

    # Ensure the fetched user matches the created user
    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.name == user_create_data.name
    assert fetched_user.email == user_create_data.email
    assert fetched_user.phone == user_create_data.phone
    assert fetched_user.role == user_create_data.role

def test_get_user_by_id_not_found(db_session, user_crud):
    """Test getting a user by ID when the user does not exist."""
    non_existing_user_id = 9999  # Assume this ID does not exist
    fetched_user = user_crud.get_user_by_id(db_session, non_existing_user_id)

    # Ensure that no user is found
    assert fetched_user is None

def test_update_user(db_session, user_crud):
    """Test the update_user method in UserCRUD."""

    # Step 1: Create a user first
    user_create_data = CreateUserSchema(
        name="John Doe",
        email="johndoe@example.com",
        phone="+1234567890",
        role="User",
        password="securepassword123"
    )
    created_user = user_crud.create_user(db_session, user_create_data)

    # Step 2: Update specific fields of the user
    updated_user = user_crud.update_user(
        db=db_session,
        user_id=created_user.id,
        name="John Updated",
        phone="+9876543210"
    )

    # Step 3: Fetch the updated user
    fetched_user = user_crud.get_user_by_id(db_session, created_user.id)

    # Assertions to verify the updates
    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.name == "John Updated"
    assert fetched_user.phone == "+9876543210"
    assert fetched_user.email == "johndoe@example.com"  # Ensure other fields remain unchanged
    assert fetched_user.role == "User"

def test_update_user_invalid_field(db_session, user_crud):
    """Test updating a user with an invalid field in UserCRUD."""
    
    # Step 1: Create a user
    user_create_data = CreateUserSchema(
        name="Jane Doe",
        email="janedoe@example.com",
        phone="+1122334455",
        role="Admin",
        password="securepassword321"
    )
    created_user = user_crud.create_user(db_session, user_create_data)

    # Step 2: Attempt to update with an invalid field
    with pytest.raises(ValueError, match="Invalid field: invalid_field"):
        user_crud.update_user(
            db=db_session,
            user_id=created_user.id,
            invalid_field="some_value"
        )

def test_update_user_not_found(db_session, user_crud):
    """Test updating a user that does not exist in UserCRUD."""
    
    # Attempt to update a non-existing user
    non_existing_user_id = 9999  # Assume this ID does not exist
    with pytest.raises(ValueError, match="User not found."):
        user_crud.update_user(
            db=db_session,
            user_id=non_existing_user_id,
            name="Non Existent"
        )

