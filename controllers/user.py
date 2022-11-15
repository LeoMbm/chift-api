from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

# from app.core.security import get_password_hash, verify_password
from controllers.base import CRUDBase
from core.security import get_password_hash, verify_password

from models.Users import UserAccount
from schemas.Users import UserSchema, UpdateUserModel


class CRUDUser(CRUDBase[UserAccount, UserSchema, UpdateUserModel]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserAccount]:
        return db.query(UserAccount).filter(UserAccount.email == email).first()

    def create(self, db: Session, *, obj_in: UserSchema) -> UserAccount:
        db_obj = UserAccount(
            id=obj_in.id,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            created_at=obj_in.created_at,
            updated_at=obj_in.updated_at

        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: UserAccount, obj_in: Union[UpdateUserModel, Dict[str, Any]]
    ) -> UserAccount:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[UserAccount]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


account = CRUDUser(UserAccount)
