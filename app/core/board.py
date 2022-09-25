from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from fastapi_pagination import paginate as array_paginate
from fastapi.encoders import jsonable_encoder

from app.models.user import User
from app.models.board import Board, BoardUser, Card
from app.models.enums.board import UserRoleType
from app.models.enums import State, Status
from app.models.enums.board import BoardStatus
from app.helpers.error_helper import ErrorCode as errors
from app.api.v1.schemas.board import BoardUpdateIn, CardIn, CardUpdateIn
from app.core.user import UserCore


class BoardCore:
    def __init__(self, db):
        self.db = db

    # Base Function
    def get_board_by_id(self, board_id: int, board_status=None, show_error: bool = True) -> Board:
        """
        This function checks if there is a board belonging to the given ID number
        :param board_id: ID number of the requested board
        :param board_status: The list must be given (e.g. [BoardStatus.active, BoardStatus.archived]
        :param show_error: Specifies whether to give an error when the board is not found. If given false, the empty object is returned
        :return: Board Object
        """
        if board_status is None:
            board_status = [BoardStatus.active, BoardStatus.archived]

        board = self.db.query(Board).filter(Board.id == board_id, Board.status.in_(board_status)).first()

        if not board and show_error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors.board_not_found)

        return board

    def get_card_by_id(self, board: Board, card_id: int, show_error: bool = True) -> Card:
        """
        This function checks the existence of the card whose ID number is given in the given board
        :param board: The board to control the card
        :param card_id: ID number of the requested card
        :param show_error: Specifies whether to give an error when the card is not found. If given false, the empty object is returned
        :return: Card Object
        """
        card = (
            self.db.query(Card)
            .filter(Card.id == card_id, Card.board_id == board.id)
            .filter(Card.status == Status.active)
            .first()
        )

        if not card and show_error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors.card_not_found)

        return card

    def check_board_member(self, board: Board, user: User, role=None, show_error: bool = True) -> BoardUser:
        """
        This function checks whether the given user is a member of the given board
        :param board: The board where the user's membership will be checked
        :param user: User to search in board
        :param role: Determines in which role the user will be searched (default: Owner and Member)
        :param show_error: Specifies whether to give an error when the member is not found. If given false, the empty object is returned
        :return: BoardUser Object
        """
        if role is None:
            role = [UserRoleType.member, UserRoleType.owner]

        filter_array = [
            BoardUser.board_id == board.id,
            BoardUser.user_id == user.id,
            BoardUser.status == State.approved,
            BoardUser.role.in_(role)
        ]

        board_user = (
            self.db.query(BoardUser)
            .filter(*filter_array)
            .first()
        )

        if not board_user and show_error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors.user_not_member_the_board)

        return board_user

    # Crud Functions
    def create_board(self, user: User, name: str, description: str = None) -> dict:
        # TODO: Check if there is a different board with the same name that the user is owner.

        board = Board()
        board.name = name
        board.description = description

        self.db.add(board)
        self.db.flush()

        owner = BoardUser()
        owner.user_id = user.id
        owner.board_id = board.id
        owner.role = UserRoleType.owner
        owner.status = State.approved

        self.db.add(owner)
        self.db.commit()

        return {"message": "Pano oluşturuldu", "id": board.id}

    def get_all_boards(self, user: User, search: str = None, role: UserRoleType = None):
        filter_array = []

        if search:
            search = "%{}%".format(search)
            filter_array.append(Board.name.ilike(search))  # noqa

        if role:
            filter_array.append(BoardUser.role == role)

        boards = (
            self.db.query(Board)
            .join(BoardUser, BoardUser.board_id == Board.id)
            .filter(BoardUser.user_id == user.id, BoardUser.status == State.approved)
            .filter(Board.status != BoardStatus.deleted)
            .filter(*filter_array)
            .with_entities(
                Board.id,
                Board.name,
                Board.description,
                Board.status,
                Board.date_created,
                Board.date_modified,
                BoardUser.role,
            )
        )

        return sqlalchemy_paginate(boards)

    def get_board_detail(self, board_id: int) -> dict:
        return jsonable_encoder(self.get_board_by_id(board_id=board_id))

    def update_board(self, board, update_schema: BoardUpdateIn) -> dict:
        unset_fields = update_schema.dict(exclude_unset=True)

        for key in unset_fields.keys():
            setattr(board, key, unset_fields.get(key))

        self.db.commit()

        return {"message": "Kart başarıyla düzenlendi"}

    def delete_board(self, board: Board):
        if board.status == BoardStatus.deleted:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.board_already_deleted)

        board.status = BoardStatus.deleted
        self.db.commit()

        return {"message": "Pano başarıyla silindi."}

    def get_board_users(self, board: Board):
        board_users = (
            self.db.query(BoardUser)
            .join(User, BoardUser.user_id == User.id)
            .filter(BoardUser.board_id == board.id, BoardUser.status == State.approved)
            .with_entities(
                BoardUser.id,
                BoardUser.date_created,
                BoardUser.date_modified,
                BoardUser.user_id,
                User.full_name,
                BoardUser.role,
            )
        )

        return sqlalchemy_paginate(board_users)

    def add_board_user(self, board: Board, user: User, role: UserRoleType) -> dict:
        check_user_member = self.check_board_member(board=board, user=user, show_error=False)

        if check_user_member:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.user_already_exists_in_board)

        board_member = BoardUser()
        board_member.board_id = board.id
        board_member.user_id = user.id
        board_member.role = role
        board_member.status = State.approved  # TODO: change here when adding invite future

        self.db.add(board_member)
        self.db.commit()

        return {"message": "Kullanıcı panoya eklendi"}

    def update_board_user(self, board: Board, user: User, role: UserRoleType) -> dict:
        # TODO: Block owner role change if no other admins.
        check_user_member = self.check_board_member(board=board, user=user)
        check_user_member.role = role
        self.db.commit()

        return {"message": "Kullanıcının pano rolü güncellendi."}

    def delete_board_user(self, board: Board, user: User) -> dict:
        # TODO: Block deletion if no other admins.
        check_user_member = self.check_board_member(board=board, user=user, show_error=True)

        self.db.delete(check_user_member)
        self.db.commit()

        return {"message": "Kullanıcı panodan silindi."}

    def create_card(self, board: Board, owner: User, create_schema: CardIn):
        if create_schema.assignment_id is not None:
            user = UserCore(self.db).get_user_by_id(create_schema.assignment_id)

            self.check_board_member(board=board, user=user)

            assignment = user.id
        else:
            assignment = None

        card = Card()
        card.board_id = board.id
        card.owner_id = owner.id
        card.assignment_id = assignment
        card.title = create_schema.title
        card.content = create_schema.content
        card.estimated_start = create_schema.estimated_start
        card.estimated_finish = create_schema.estimated_finish
        card.finish_date = create_schema.finish_date
        card.state = create_schema.state

        self.db.add(card)
        self.db.commit()

        return {"message": "Kart başarıyla oluşturuldu", "id": card.id}

    def get_all_cards(self, board: Board):
        cards = (
            self.db.query(Card)
            .filter(Card.board_id == board.id)
            .filter(Card.status == Status.active)
        )

        return sqlalchemy_paginate(cards)

    def get_card_detail(self, board: Board, card_id: int):
        return jsonable_encoder(self.get_card_by_id(board=board, card_id=card_id))

    def update_card(self, card: Card, update_schema: CardUpdateIn) -> dict:
        unset_fields = update_schema.dict(exclude_unset=True)

        for key in unset_fields.keys():
            setattr(card, key, unset_fields.get(key))

        self.db.commit()

        return {"message": "Kart başarıyla düzenlendi"}

    def delete_card(self, card: Card) -> dict:
        card.status = Status.deleted
        self.db.commit()

        return {"message": "Kart başarıyla slindi"}
