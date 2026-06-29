from datetime import datetime
from src.tickets.enums import TicketStatus
from pydantic import BaseModel, ConfigDict


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketUpdate(BaseModel):
    status: TicketStatus


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
    category: str | None
    priority: str |None
    customer_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )