from datetime import timedelta
from typing import Any

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import xmlrpc.client

from fastapi.middleware.cors import CORSMiddleware

from api.utils import get_current_user, connect_to_odoo_instance, get_user_from_odoo
from controllers.user import account
from core import security
from core.settings import settings
from db.initdb import get_db
from models.Users import UserAccount
from schemas.Users import UserSchema, ResponseModel
from schemas.Token import Token

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def RegisterUserView(
        user_in: UserSchema, db: Session = Depends(get_db)
):
    """
    Sign up a user and hashinh his password.
    """
    # Try to retrieve the user with email and if exists throw exception
    user = account.get_by_email(db, email=user_in.email)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = account.create(db, obj_in=user_in)
    return ResponseModel(user, "User created")


@app.post("/login", response_model=Token)
def LoginUserView(
        db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Sign in a user and giving him a jwt token.
    """
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
def GetUserViaTokenView(db: Session = Depends(get_db), current_user: UserAccount = Depends(get_current_user),
                       ) -> Any:
    """
    Get current user.
    """
    return current_user


@app.get("/odoo")
def UserFromOdooView(current_user: UserAccount = Depends(get_current_user)):
    """
    Get user from Odoo Instance
    """
    uid = connect_to_odoo_instance(settings.CHIFT_URL,
                                    settings.CHIFT_DB,
                                    settings.CHIFT_USERNAME,
                                    settings.CHIFT_PASSWORD)
    if not uid:
        raise HTTPException(status_code=400, detail="Unable to connect to Chift instance")
    data = get_user_from_odoo(settings.CHIFT_URL,
                              settings.CHIFT_DB,
                              uid,
                              settings.CHIFT_PASSWORD)
    return data
