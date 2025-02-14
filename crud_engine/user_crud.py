from typing import Optional  
from sqlalchemy.orm import Session
from models.models import CreateUser  
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

    def get_user_by_email(self, db: Session, email: str) -> Optional[CreateUser]:
        """Gets a user by their email from the database.

        Args:
            db: The database session.
            email: The email of the user to retrieve.

        Returns:
            The user object if found, None otherwise.
        """
        return db.query(CreateUser).filter(CreateUser.email == email).first()

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[CreateUser]:
        """Gets a user by their ID from the database.

        Args:
            db: The database session.
            user_id: The ID of the user to retrieve.

        Returns:
            The user object if found, None otherwise.
        """
        return db.query(CreateUser).filter(CreateUser.id == user_id).first()

    def update_user(self, db: Session, user_id: int, **kwargs) -> CreateUser:
        """
        Updates the user data based on the provided fields.

        Args:
            db: The database session.
            user_id: The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the fields to update and their new values.

        Returns:
            The updated user object.

        Raises:
            ValueError: If no valid fields are provided for the update.
        """
        user = self.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("User not found.")

        # Update the fields in the user object
        for key, value in kwargs.items():
            if hasattr(user, key):  # Ensure the user model has the attribute
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid field: {key}")

        db.commit()
        db.refresh(user)
        return user

