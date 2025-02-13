from sqlalchemy.orm import Session
from models.models import CreateUser  # Assuming CreateUser is the model from models.py
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

    def get_user_by_email(self, db: Session, email: str) -> CreateUser:
        """Gets a user by their email from the database.

        Args:
            db: The database session.
            email: The email of the user to retrieve.

        Returns:
            The user object if found, None otherwise.
        """
        return db.query(CreateUser).filter(CreateUser.email == email).first()

    def get_user_by_id(self, db: Session, user_id: int) -> CreateUser:
        """Gets a user by their ID from the database.

        Args:
            db: The database session.
            user_id: The ID of the user to retrieve.

        Returns:
            The user object if found, None otherwise.
        """
        return db.query(CreateUser).filter(CreateUser.id == user_id).first()
