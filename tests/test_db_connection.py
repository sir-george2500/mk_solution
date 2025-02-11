import pytest
from unittest.mock import patch, MagicMock
from config.db import db_connection
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

@pytest.fixture
def mock_session():
    """
    Creates a mock session for testing purposes.
    """
    return MagicMock(spec=Session)

@patch('config.db.create_engine')
@patch('config.db.sessionmaker')
def test_db_connection_exists(mock_sessionmaker, mock_create_engine):
    """
    Test that the db_connection function exists.
    """
    assert hasattr(db_connection, '__call__'), "db_connection function does not exist"

@patch('config.db.create_engine')
@patch('config.db.sessionmaker')
def test_db_connection_successful(mock_sessionmaker, mock_create_engine, mock_session):
    """
    Test that the db_connection function successfully establishes a database connection using SQLAlchemy.
    """
    db_url = os.getenv("DB_URL")
    
    # Set up mock session
    mock_sessionmaker.return_value = mock_session

    # Call the function to connect to the database
    result = db_connection()

    # Assert that the function returned a session object
    assert isinstance(result, MagicMock), "Failed to establish a database connection"

    # Assert that create_engine was called with the correct parameters
    mock_create_engine.assert_called_once_with(db_url)
