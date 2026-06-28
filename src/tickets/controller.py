from sqlalchemy.orm import Session

from src.tickets.models import Ticket
from src.tickets.schemas import TicketCreate
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