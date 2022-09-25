from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.task import TaskCore

router = APIRouter()


@router.get("/card-start-reminder", summary="Send a message to cardholders whose estimated start date has passed")
def card_start_reminder(
    db: Session = Depends(get_db),
):
    return TaskCore(db).card_start_reminder()


@router.get("/card-finish-reminder", summary="Send a message to the admin for cards past the estimated start date.")
def card_finish_reminder(
    db: Session = Depends(get_db),
):
    return TaskCore(db).card_finish_reminder()
