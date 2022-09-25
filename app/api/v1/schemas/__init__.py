from datetime import datetime

from pydantic import BaseModel


class BaseOutModel(BaseModel):
    id: int
    date_created: datetime
    date_modified: datetime


class MessageOut(BaseModel):
    message: str


class MessageOutWithID(MessageOut):
    id: int
