from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from src.utils.db import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(Text, nullable=False)

    status = Column(
        String(50),
        default="Open",
        nullable=False
    )

    category = Column(String(100))

    priority = Column(String(50))

    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    created_at = Column(
    DateTime,
    default=lambda: datetime.now(UTC)
    )

    updated_at = Column(
    DateTime,
    default=lambda: datetime.now(UTC),
    onupdate=lambda: datetime.now(UTC)
    )
    customer = relationship("User",back_populates="tickets")