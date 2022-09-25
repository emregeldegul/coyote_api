from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel, PositiveInt

from app.api.v1.schemas import BaseOutModel
from app.models.enums.board import BoardStatus, UserRoleType, CardState


class BoardIn(BaseModel):
    name: str = Field(title="Board Name", description="Name of the board", max_length=100)
    description: Optional[str] = Field(title="Board Description")


class BoardOut(BoardIn, BaseOutModel):
    status: BoardStatus = Field(title="Board Status")
    role: UserRoleType = Field(title="User Role", description="User role in the board")


class BoardDetailOut(BoardIn, BaseOutModel):
    status: BoardStatus = Field(title="Board Status")


class BoardUpdateIn(BoardIn):
    status: BoardStatus = Field(title="Board Status")


class BoardUserOut(BaseOutModel):
    user_id: int = Field(title="User ID", description="ID number the user")
    full_name: str = Field(title="User Full Name", description="User Full Name")
    role: UserRoleType = Field(title="User Role", description="User role in the board")

    class Config:
        orm_mode = True


class CardIn(BaseModel):
    assignment_id: Optional[PositiveInt] = Field(None, title="Assignment", description="The user to whom the card is assigned")
    title: str = Field(title="Card Title", description="Title of the card", max_length=150)
    content: Optional[str] = Field(title="Card Content", description="Content of the card")
    estimated_start: Optional[datetime] = Field(title="Estimated Start", description="Estimated start date of the card")
    estimated_finish: Optional[datetime] = Field(title="Estimated Finish", description="Estimated completion date of the card")
    finish_date: Optional[datetime] = Field(title="Estimated Finish", description="Completion date of the card")
    state: Optional[CardState] = Field(title="Card State", description="Current status of the card")


class CardUpdateIn(CardIn):
    title: Optional[str] = Field(title="Card Title", description="Title of the card", max_length=150)


class CardOut(CardIn, BaseOutModel):
    class Config:
        orm_mode = True

