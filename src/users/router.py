from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.users.auth import get_current_user,get_current_customer,get_current_agent
from src.users.models import User

from src.users.controller import login_user, register_user
from src.users.schemas import (
    Token,
    UserLogin,
    UserRegister,
    UserResponse,
)
from src.utils.db import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    return register_user(db, user)


@router.post(
    "/login",
    response_model=Token
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return login_user(db, user)