from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from controllers.user import account
from core import security
from core.settings import settings
from db.initdb import get_db
from models.Users import UserAccount
from schemas.Token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/login"
)


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> UserAccount:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = account.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
