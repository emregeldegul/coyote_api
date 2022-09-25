from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.user import UserCore
from app.db.database import get_db
from app.helpers.error_helper import ErrorCode as errors
from app.helpers.token_helper import verify_access_token
from app.models.enums import Status
from app.models.user import User
from settings import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/" + settings.APP_VERSION + "/auth/login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    token_data = verify_access_token(token)
    user = UserCore(db).get_user_by_email(email=token_data["email"], user_status=[Status.active, Status.passive])

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.status != Status.active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.inactive_user)

    return current_user
