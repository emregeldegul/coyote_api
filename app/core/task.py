from datetime import datetime

from app.helpers.email_helper import send_template_mail
from app.models.board import Board, Card
from app.models.enums.board import BoardStatus, CardState
from app.models.user import User


class TaskCore:
    def __init__(self, db):
        self.db = db

    def card_start_reminder(self):
        now = datetime.now()
        check_cards = (
            self.db.query(Card)
            .join(Board, Card.board_id == Board.id)
            .join(User, Card.owner_id == User.id)
            .filter(Board.status == BoardStatus.active)
            .filter(Card.estimated_start <= now, Card.state == CardState.todo)
            .with_entities(
                User.email,
                User.full_name,
                Card.title,
                Board.name,
                Card.estimated_start,
            )
            .all()  # TODO:  use iterator
        )

        for card in check_cards:
            send_template_mail(
                template_path="card_start_reminder.html",
                template_vars={
                    "full_name": card.full_name,
                    "board_name": card.name,
                    "card_title": card.title,
                    "estimated_start": card.estimated_start,
                },
                subject="Hatırlatma",
                receivers=card.email,
            )

    def card_finish_reminder(self):
        now = datetime.now()
        check_cards = (
            self.db.query(Card)
            .join(Board, Card.board_id == Board.id)
            .join(User, Card.owner_id == User.id)
            .filter(Board.status == BoardStatus.active)
            .filter(Card.estimated_finish <= now, Card.state != CardState.done)
            .with_entities(
                User.email,
                User.full_name,
                Card.title,
                Board.name,
                Card.estimated_finish,
            )
            .all()
        )

        for card in check_cards:
            send_template_mail(
                template_path="card_finish_reminder.html",
                template_vars={
                    "full_name": card.full_name,
                    "board_name": card.name,
                    "card_title": card.title,
                    "estimated_finish": card.estimated_finish,
                },
                subject="Hatırlatma",
                receivers=card.email,
            )
