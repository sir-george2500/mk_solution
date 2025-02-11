from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models.models import Base

# Load environment variables from the .env file
load_dotenv()

def db_connection():
    """
    Establishes a database connection using SQLAlchemy.

    Returns:
        A SQLAlchemy session object.
    """
    # Retrieve database connection details from environment variables
    db_url = os.getenv("DB_URL")

    # Check if the DB_URL is None or empty
    if not db_url:
        raise ValueError("Database URL is not set in environment variables.")

    # Build the connection URL for SQLAlchemy
    connection_url = db_url

    try:
        # Create an SQLAlchemy engine
        engine = create_engine(connection_url)

        # Create the base
        Base.metadata.create_all(bind=engine)

        # Create a session factory
        Session = sessionmaker(bind=engine)

        # Create and return a session
        session = Session()
        return session

    except Exception as e:
        # Handle connection errors (e.g., log the error, raise an exception)
        print(f"Failed to establish a database connection: {e}")
        raise

