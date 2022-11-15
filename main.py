from datetime import timedelta
from typing import Any

from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.utils import get_current_user
from controllers.user import account
from core import security
from core.settings import settings
from db.initdb import get_db
from models.Users import UserAccount
from schemas.Users import UserSchema, ResponseModel
from schemas.Token import Token

app = FastAPI()


@app.post("/register")
def register_user(
        user_in: UserSchema, db: Session = Depends(get_db)
):
    user = account.get_by_email(db, email=user_in.email)
    print(user_in)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = account.create(db, obj_in=user_in)
    return ResponseModel(user, "User created")


@app.post("/login", response_model=Token)
def login_user(
        db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = account.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@app.get("/user", response_model=UserSchema)
def get_user_via_token(db: Session = Depends(get_db), current_user: UserAccount = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
