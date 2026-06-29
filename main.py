from fastapi import FastAPI
from src.tickets.router import router as ticket_router
from src.utils.db import Base, engine
from src.users.models import User
from src.tickets.models import Ticket
from src.users.router import router as user_router
from src.ai.router import router as ai_router
# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Support Ticket System",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(ticket_router)
app.include_router(ai_router)
@app.get("/")
def root():
    return {
        "message": "AI Support Ticket System API"
    }