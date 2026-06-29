from pydantic import BaseModel
from typing import Optional

class TicketAnalysis(BaseModel):
    category: str
    priority: str
    summary: str

class TicketSearchFilters(BaseModel):
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    keyword: Optional[str] = None

class AIInsightsResponse(BaseModel):
    total_tickets: int
    open_tickets: int
    closed_tickets: int
    top_category: str
    top_priority: str
    ai_summary: str