from datetime import datetime, UTC
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.utils.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    hashed_password = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False, default="customer")

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )

    tickets = relationship(
        "Ticket",
        back_populates="customer",
        cascade="all, delete-orphan"
    )