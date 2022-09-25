from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.schemas.user import UserDetailOut
from app.db.database import get_db
from app.models.user import User
from app.core.user import UserCore
from app.api.v1.dependencies import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=UserDetailOut)
def get_current_user_detail(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return UserCore(db).get_user_detail(current_user)
