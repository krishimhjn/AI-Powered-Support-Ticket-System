from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from src.tickets.controller import create_ticket,get_my_tickets,get_all_tickets,update_ticket_status,get_ticket_by_id
from src.tickets.schemas import TicketCreate, TicketResponse,TicketUpdate
from src.users.auth import get_current_customer,get_current_agent,get_current_user
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

@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket_by_id_endpoint(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = get_ticket_by_id(
        db=db,
        ticket_id=ticket_id
    )

    # Customer can only view their own ticket
    if (
        current_user.role == "customer"
        and ticket.customer_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied."
        )

    return ticket