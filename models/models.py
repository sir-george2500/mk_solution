from sqlalchemy import Boolean, String, Integer, DateTime, Text, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[str | None] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    forget_password_token: Mapped[str | None] = mapped_column(String, nullable=True)
    forget_password_token_expiry: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    forget_password_token_used: Mapped[bool] = mapped_column(Boolean, default=False)
    verify_user_token: Mapped[str | None] = mapped_column(String, nullable=True)
    verify_user_token_expiry: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verify_user_token_used: Mapped[bool] = mapped_column(Boolean, default=False)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    profile_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    business_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_onboarded: Mapped[bool] = mapped_column(Boolean, default=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

