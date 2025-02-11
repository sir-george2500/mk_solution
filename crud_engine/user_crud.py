from sqlalchemy.orm import Session
from models.models import CreateUser  # Assuming CreateUser is the model from models.py
from fastapi import HTTPException
from models.schemas.user_schemas import CreateUserSchema

class UserCRUD:
    """Handles create, read, update, and delete (CRUD) operations for users."""

    def create_user(self, db: Session, user_create: CreateUserSchema) -> CreateUser:
        """Creates a new user in the database.

        Args:
            db: The database session.
            user_create: A UserCreate schema instance containing user data.

        Returns:
            The newly created user object.
        """

        user_data = user_create.model_dump()
        user = CreateUser(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
