from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.tickets.controller import create_ticket,get_my_tickets,get_all_tickets,update_ticket_status
from src.tickets.schemas import TicketCreate, TicketResponse,TicketUpdate
from src.users.auth import get_current_customer,get_current_agent
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

@router.get(
    "/my-tickets",
    response_model=list[TicketResponse]
)
def get_my_tickets_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    return get_my_tickets(
        db=db,
        current_user=current_user
    )

@router.get(
    "/",
    response_model=list[TicketResponse]
)
def get_all_tickets_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agent)
):
    return get_all_tickets(db)

@router.patch(
    "/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket_status_endpoint(
    ticket_id: int,
    ticket_update: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agent)
):
    return update_ticket_status(
        db=db,
        ticket_id=ticket_id,
        ticket_update=ticket_update
    )