from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.tickets.controller import create_ticket
from src.tickets.schemas import TicketCreate, TicketResponse
from src.users.auth import get_current_customer
from src.users.models import User
from src.utils.db import get_db

router = APIRouter(prefix="/tickets",tags=["Tickets"])

@router.post("/",response_model=TicketResponse)
def create_ticket_endpoint(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    return create_ticket(
        db=db,
        ticket=ticket,
        current_user=current_user
    )