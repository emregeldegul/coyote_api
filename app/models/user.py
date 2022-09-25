from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    String,
)
from sqlalchemy.orm import column_property

from app.models.base import BaseModel
from app.models.enums import Status


class User(BaseModel):
    __tablename__ = "user"  # noqa

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = column_property(first_name + " " + last_name)
    email = Column(String(50), nullable=False)
    email_verification = Column(Boolean, nullable=False, default=False)
    email_verification_date = Column(DateTime, nullable=True)
    email_verification_code = Column(String(50), nullable=False)
    email_verification_code_exp_date = Column(DateTime, nullable=False, default=datetime.now())
    password_hash = Column(String(120), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.active)
