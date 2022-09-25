from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.api.v1.schemas import MessageOut
from app.api.v1.schemas.auth import (
    EmailVerificationIn,
    LoginOut,
    PasswordResetIn,
    RegisterIn,
)
from app.core.auth import AuthCore
from app.core.user import UserCore
from app.db.database import get_db

router = APIRouter()


@router.post("/login", response_model=LoginOut)
def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return AuthCore(db).login_user(form_data.username, form_data.password)  # noqa


@router.post("/register", response_model=MessageOut)
def user_register(
    register_schema: RegisterIn,
    db: Session = Depends(get_db),
):
    return UserCore(db).create_user(
        first_name=register_schema.first_name,
        last_name=register_schema.last_name,
        email=register_schema.email,
        password=register_schema.password,
    )


@router.post("/email-verification", response_model=MessageOut, summary="Verify E-Mail")
def email_verification(
    verification_schema: EmailVerificationIn,
    db: Session = Depends(get_db),
):
    return AuthCore(db).verify_email(email=verification_schema.email, code=verification_schema.code)


@router.post("/password-reset", response_model=MessageOut, summary="Reset Password")
def password_reset(
    reset_schema: PasswordResetIn,
    db: Session = Depends(get_db),
):
    return AuthCore(db).user_password_reset(
        email=reset_schema.email, code=reset_schema.code, new_password=reset_schema.password
    )


@router.get("/password-reset/{email_address}", response_model=MessageOut)
def send_password_reset_mail(
    email_address: EmailStr,
    db: Session = Depends(get_db),
):
    return AuthCore(db).send_password_reset_mail(email=email_address)
