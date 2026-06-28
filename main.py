from fastapi import FastAPI

from src.utils.db import Base, engine
from src.users.models import User
from src.users.router import router as user_router

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Support Ticket System",
    version="1.0.0"
)

app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": "AI Support Ticket System API"
    }