from typing import Optional, List  
from sqlalchemy.orm import Session
from models.models import User  
from models.schemas.user_schemas import CreateUserSchema


class UserCRUD:
    """Handles create, read, update, and delete (CRUD) operations for users."""

    def create_user(self, db: Session, user_create: CreateUserSchema) -> User:
        """Creates a new user in the database.

        Args:
            db: The database session.
            user_create: A UserCreate schema instance containing user data.

        Returns:
            The newly created user object.
        """
        user_data = user_create.model_dump()
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Gets a user by their email from the database.

        Args:
            db: The database session.
            email: The email of the user to retrieve.

        Returns:
            The user object if found, None otherwise.
        """
        return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Gets a user by their ID from the database.

        Args:
            db: The database session.
            user_id: The ID of the user to retrieve.

        Returns:
            The user object if found, None otherwise.
        """
        return db.query(User).filter(User.id == user_id).first()

    def update_user(self, db: Session, user_id: int, **kwargs) -> User:
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
    
    def get_onboarded_clients(self, db: Session) -> List[User]:
        """Gets all clients who have uploaded their business certificates."""
        return db.query(User).filter(
            User.role == "client",
            User.is_onboarded == True
        ).all()

# Create an instance of UserCRUD
crud = UserCRUD()
