from sqlalchemy import Boolean, Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class CreateUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=True)
    password = Column(String, nullable=False)
    forget_password_token = Column(String, nullable=True)
    forget_password_token_expiry = Column(DateTime(timezone=True), nullable=True)
    forget_password_token_used = Column(Boolean, default=False)
    verify_user_token = Column(String, nullable=True)
    verify_user_token_expiry = Column(DateTime(timezone=True), nullable=True)
    verify_user_token_used = Column(Boolean, default=False)
    profile_url = Column(Text, nullable=True)
    address = Column(String, nullable=True)
    business_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

