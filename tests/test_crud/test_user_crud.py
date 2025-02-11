from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import CreateUser, Base
from crud_engine.user_crud import UserCRUD
from models.schemas.user_schemas import CreateUserSchema


@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def crud():
    return UserCRUD()

def test_create_user(db_engine, crud):
    Session = sessionmaker(bind=db_engine)
    db = Session()
    
    # Ensure valid URLs and datetime format
    user_data = {
        "name": "Alice Green",
        "email": "alicegreen@example.com",
        "phone": "+1234567890",
        "role": "Manager",
        "profile_url": "https://example.com/profile/alice-green", 
        "address": "123 Elm Street, Springfield",
        "business_url": "https://alicegreenbusiness.com",
        "created_at": datetime.now(), 
        "updated_at": datetime.now(), 
    }

    # Convert string URLs and datetime fields if necessary
    user_create = CreateUserSchema(**user_data)
    
    # Now that we have a valid user_create, create the user in the DB
    user = crud.create_user(db, user_create)
    
    # Assertions to validate if the user is created correctly
    assert isinstance(user, CreateUser)  
    assert user.name == user_data["name"]
    assert user.email == user_data["email"]
    assert user.created_at == user_data["created_at"]
    assert user.updated_at == user_data["updated_at"]

