from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_active_user
from app.api.v1.schemas import MessageOut, MessageOutWithID
from app.api.v1.schemas.board import (
    BoardDetailOut,
    BoardIn,
    BoardOut,
    BoardUpdateIn,
    BoardUserOut,
    CardIn,
    CardOut,
    CardUpdateIn,
)
from app.core.board import BoardCore
from app.core.user import UserCore
from app.db.database import get_db
from app.helpers.error_helper import ErrorCode as errors
from app.models.enums.board import BoardStatus, UserRoleType
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=MessageOutWithID, summary="Create a new board")
def create_board(
    create_schema: BoardIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return BoardCore(db).create_board(user=current_user, name=create_schema.name, description=create_schema.description)


@router.get(
    "/", response_model=Page[BoardOut], summary="List the boards where the current user is a member or an owner"
)
def get_all_boards(
    search: Optional[str] = None,
    role: Optional[UserRoleType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return BoardCore(db).get_all_boards(user=current_user, search=search, role=role)


@router.get(
    "/{board_id}", response_model=BoardDetailOut, summary="View board details where current user is a member or owner"
)
def get_board_detail(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    check_board = BoardCore(db).get_board_by_id(board_id=board_id)
    check_board_member = BoardCore(db).check_board_member(board=check_board, user=current_user)  # noqa

    return BoardCore(db).get_board_detail(board_id=check_board.id)


@router.put("/{board_id}", response_model=MessageOut, summary="Update the board you are owner")
def update_board(
    board_id: int,
    update_schema: BoardUpdateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Only the owners of the add can update board
    """
    board = BoardCore(db).get_board_by_id(board_id)
    board_member = BoardCore(db).check_board_member(
        board=board, user=current_user, role=[UserRoleType.owner], show_error=False
    )

    if not board_member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=errors.user_not_owner_the_board)

    return BoardCore(db).update_board(board=board, update_schema=update_schema)


@router.delete("/{board_id}", response_model=MessageOut, summary="")
def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Only the owners of the board can delete.
    """
    board = BoardCore(db).get_board_by_id(board_id)
    board_member = BoardCore(db).check_board_member(
        board=board, user=current_user, role=[UserRoleType.owner], show_error=False
    )

    if not board_member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=errors.user_not_owner_the_board)

    return BoardCore(db).delete_board(board=board)


@router.get("/{board_id}/user", response_model=Page[BoardUserOut])
def get_board_users(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    board = BoardCore(db).get_board_by_id(board_id)
    return BoardCore(db).get_board_users(board=board)


@router.post("/{board_id}/user/{user_id}", response_model=MessageOut)
def add_board_user(
    board_id: int,
    user_id: int,
    role: UserRoleType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Only the owners of the board can add a member
    """
    board = BoardCore(db).get_board_by_id(board_id=board_id)
    board_member = BoardCore(db).check_board_member(
        board=board, user=current_user, role=[UserRoleType.owner], show_error=False
    )

    if not board_member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=errors.user_not_owner_the_board)

    user = UserCore(db).get_user_by_id(user_id=user_id)

    return BoardCore(db).add_board_user(board=board, user=user, role=role)


@router.put("/{board_id}/user/{user_id}", response_model=MessageOut)
def update_board_user(
    board_id: int,
    user_id: int,
    role: UserRoleType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Only the owners of the board can update a member
    """
    board = BoardCore(db).get_board_by_id(board_id=board_id)
    board_member = BoardCore(db).check_board_member(
        board=board, user=current_user, role=[UserRoleType.owner], show_error=False
    )

    if not board_member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=errors.user_not_owner_the_board)

    user = UserCore(db).get_user_by_id(user_id=user_id)

    return BoardCore(db).update_board_user(board=board, user=user, role=role)


@router.delete("/{board_id}/user/{user_id}", response_model=MessageOut)
def delete_board_user(
    board_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Only the owners of the board can delete a member.
    """
    board = BoardCore(db).get_board_by_id(board_id=board_id)
    board_member = BoardCore(db).check_board_member(
        board=board, user=current_user, role=[UserRoleType.owner], show_error=False
    )

    if not board_member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=errors.user_not_owner_the_board)

    user = UserCore(db).get_user_by_id(user_id=user_id)

    return BoardCore(db).delete_board_user(board=board, user=user)


@router.post("/{board_id}/card", response_model=MessageOut, summary="Create a card for the board")
def create_card(
    board_id: int,
    create_schema: CardIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    board = BoardCore(db).get_board_by_id(board_id=board_id, board_status=[BoardStatus.active])
    board_member = BoardCore(db).check_board_member(board=board, user=current_user)  # noqa

    return BoardCore(db).create_card(board=board, owner=current_user, create_schema=create_schema)


@router.get("/{board_id}/card", response_model=Page[CardOut])
def get_all_cards(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    board = BoardCore(db).get_board_by_id(board_id=board_id)
    board_member = BoardCore(db).check_board_member(board=board, user=current_user)  # noqa

    return BoardCore(db).get_all_cards(board=board)


@router.get("/{board_id}/card/{card_id}", response_model=CardOut, summary="Returns the card detail of a board")
def get_card_detail(
    board_id: int,
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    board = BoardCore(db).get_board_by_id(board_id=board_id)
    board_member = BoardCore(db).check_board_member(board=board, user=current_user)  # noqa

    return BoardCore(db).get_card_detail(board=board, card_id=card_id)


@router.put("/{board_id}/card/{card_id}", response_model=MessageOut)
def update_card(
    board_id: int,
    card_id: int,
    update_schema: CardUpdateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Only the owners of the board can update the card
    """
    board = BoardCore(db).get_board_by_id(board_id=board_id)
    board_member = BoardCore(db).check_board_member(board=board, user=current_user)  # noqa
    card = BoardCore(db).get_card_by_id(board=board, card_id=card_id)
    return BoardCore(db).update_card(card=card, update_schema=update_schema)


@router.delete("/{board_id}/card/{card_id}", response_model=MessageOut)
def delete_card(
    board_id: int,
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Only the owners of the board can delete a member
    """
    board = BoardCore(db).get_board_by_id(board_id=board_id)
    board_member = BoardCore(db).check_board_member(board=board, user=current_user)  # noqa
    card = BoardCore(db).get_card_by_id(board=board, card_id=card_id)
    return BoardCore(db).delete_card(card=card)
