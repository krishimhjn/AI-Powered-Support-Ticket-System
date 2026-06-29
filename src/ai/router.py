from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from src.ai.service import generate_reply,search_filters,generate_insights
from src.tickets.models import Ticket
from src.users.auth import get_current_agent
from src.users.models import User
from src.utils.db import get_db
from sqlalchemy import or_,func
from src.ai.schemas import AIInsightsResponse

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.get("/reply/{ticket_id}")
def get_ai_reply(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agent)
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

    ticket_context = f"""
Title: {ticket.title}

Category: {ticket.category}

Priority: {ticket.priority}

Customer Message:
{ticket.description}
"""

    reply = generate_reply(ticket_context)

    return {
        "ticket_id": ticket.id,
        "ai_reply": reply
    }


@router.get("/search")
def ai_search(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agent)
):
    filters = search_filters(query)

    tickets = db.query(Ticket)

    if filters.category:
        tickets = tickets.filter(
            Ticket.category == filters.category
        )

    if filters.priority:
        tickets = tickets.filter(
            Ticket.priority == filters.priority
        )

    if filters.status:
        tickets = tickets.filter(
            Ticket.status == filters.status
        )
    if filters.keyword:
        tickets = tickets.filter(
            or_(
                Ticket.title.ilike(f"%{filters.keyword}%"),
                Ticket.description.ilike(f"%{filters.keyword}%"),
                Ticket.summary.ilike(f"%{filters.keyword}%")
            )
        )

    return tickets.all()



@router.get(
    "/insights",
    response_model=AIInsightsResponse
)
def ai_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agent)
):
    total = db.query(Ticket).count()

    open_count = (
        db.query(Ticket)
        .filter(Ticket.status == "Open")
        .count()
    )

    closed_count = (
        db.query(Ticket)
        .filter(Ticket.status == "Closed")
        .count()
    )

    top_category = (
        db.query(
            Ticket.category,
            func.count(Ticket.id)
        )
        .group_by(Ticket.category)
        .order_by(func.count(Ticket.id).desc())
        .first()
    )

    top_priority = (
        db.query(
            Ticket.priority,
            func.count(Ticket.id)
        )
        .group_by(Ticket.priority)
        .order_by(func.count(Ticket.id).desc())
        .first()
    )

    stats = f"""
Total Tickets: {total}
Open Tickets: {open_count}
Closed Tickets: {closed_count}
Top Category: {top_category[0] if top_category else "N/A"}
Top Priority: {top_priority[0] if top_priority else "N/A"}
"""

    summary = generate_insights(stats)

    return {
        "total_tickets": total,
        "open_tickets": open_count,
        "closed_tickets": closed_count,
        "top_category": top_category[0] if top_category else "N/A",
        "top_priority": top_priority[0] if top_priority else "N/A",
        "ai_summary": summary
    }