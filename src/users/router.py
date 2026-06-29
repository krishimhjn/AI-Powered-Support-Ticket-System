from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.users.auth import get_current_user,get_current_customer,get_current_agent
from src.users.models import User
from fastapi.security import OAuth2PasswordRequestForm
from src.users.controller import login_user, register_user,get_all_users
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


@router.post(
    "/token",
    response_model=Token
)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    return login_user(db, user)

@router.get("/get_all_user")
def getall(db:Session=Depends(get_db)):
    return get_all_users(db)
