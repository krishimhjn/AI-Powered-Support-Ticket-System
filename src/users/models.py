from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.utils.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    hashed_password = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False, default="customer")

    created_at = Column(DateTime, default=datetime.utcnow)