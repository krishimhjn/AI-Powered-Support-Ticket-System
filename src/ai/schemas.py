from pydantic import BaseModel


class TicketAnalysis(BaseModel):
    category: str
    priority: str
    summary: str