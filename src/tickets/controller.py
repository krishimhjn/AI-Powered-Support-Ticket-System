from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.tickets.models import Ticket
from src.tickets.schemas import TicketCreate,TicketUpdate
from src.users.models import User


def create_ticket(
    db: Session,
    ticket: TicketCreate,
    current_user: User
):
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        customer_id=current_user.id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket

def get_my_tickets(db: Session,current_user: User):
    tickets = (
        db.query(Ticket)
        .filter(Ticket.customer_id == current_user.id)
        .all()
    )

    return tickets

def get_all_tickets(db: Session):
    tickets = (
        db.query(Ticket)
        .all()
    )

    return tickets




def update_ticket_status(
    db: Session,
    ticket_id: int,
    ticket_update: TicketUpdate
):
    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    ticket.status = ticket_update.status

    db.commit()
    db.refresh(ticket)

    return ticket