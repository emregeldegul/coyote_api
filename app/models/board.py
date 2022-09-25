from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text

from app.models.base import BaseModel
from app.models.enums import State, Status
from app.models.enums.board import BoardStatus, CardState, UserRoleType


class Board(BaseModel):
    __tablename__ = "board"  # noqa

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(BoardStatus), nullable=False, default=BoardStatus.active)


class BoardUser(BaseModel):
    __tablename__ = "board_user"  # noqa

    user_id = Column(Integer, ForeignKey("user.id"))
    board_id = Column(Integer, ForeignKey("user.id"))
    role = Column(Enum(UserRoleType), nullable=False, default=UserRoleType.member)
    status = Column(Enum(State), nullable=False, default=State.waiting)


class Card(BaseModel):
    __tablename__ = "card"  # noqa

    board_id = Column(Integer, ForeignKey("board.id"))
    owner_id = Column(Integer, ForeignKey("user.id"))
    assignment_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=True)
    estimated_start = Column(DateTime, nullable=True)
    estimated_finish = Column(DateTime, nullable=True)
    finish_date = Column(DateTime, nullable=True)
    state = Column(Enum(CardState), nullable=False, default=CardState.todo)
    status = Column(Enum(Status), nullable=False, default=Status.active)


class Comment(BaseModel):
    __tablename__ = "comment"  # noqa

    user_id = Column(Integer, ForeignKey("user.id"))
    content = Column(Text, nullable=False)
