from datetime import datetime

from pytz import timezone
from sqlalchemy import Column
from sqlalchemy import DateTime as OldDateTime
from sqlalchemy import Integer
from sqlalchemy.types import TypeDecorator

from app.db.database import Base
from settings import settings


class DateTime(TypeDecorator):  # noqa
    impl = OldDateTime
    cache_ok = True

    def process_bind_param(self, value, engine):
        return datetime.now(timezone(settings.APP_TIMEZONE))

    def process_result_value(self, value, engine):
        return value


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.now)
    date_modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
