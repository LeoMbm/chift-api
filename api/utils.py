from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
import xmlrpc.client
from controllers.user import account
from core import security
from core.settings import settings
from db.initdb import get_db
from models.Users import UserAccount
from schemas.Token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/login"
)


def connect_to_odoo_instance(url: str, db: str, username: str, password: str):
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})  # Authentication return an id
    return uid  # return uid and use it in get_user_from_odoo


def get_user_from_odoo(url: str, db: str, uid, password: str):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    data = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                             [[['is_public', '=', True]]],  # Retrieved public user,
                                                            # I tried with is_company true and false
                                                            # but the response is an empty array
                             {'fields': ['name', 'email', 'street', 'zip', 'country_id']})
    return data


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> UserAccount:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        ) # Decode the token for get data inside the token
        token_data = TokenPayload(**payload) # Set decoded token to the payload schema "sub" = user id
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = account.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
