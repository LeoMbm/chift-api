from datetime import datetime

from sqlalchemy import Column, String, DateTime

from db.initdb import Base


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

