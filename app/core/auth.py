from datetime import datetime, timedelta

from fastapi import HTTPException, status
from pydantic import EmailStr

from app.core.user import UserCore
from app.helpers.hash_helper import HashHelper
from app.models.enums import Status
from app.helpers.error_helper import ErrorCode as errors
from app.helpers.token_helper import create_access_token
from settings import settings
from app.models.user import User
from app.helpers.email_helper import send_template_mail


class AuthCore:
    def __init__(self, db):
        self.db = db
        self.hash_helper = HashHelper()

    def _send_password_reset_mail(self, verification_code: str):
        pass

    def _verify_code_and_exp_time(self, email: EmailStr, code: str):
        user = UserCore(self.db).get_user_by_email(email)

        if not user.email_verification_code_exp_date > datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=errors.invalid_email_verification_exp_date)

        if not user.email_verification_code == code:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.invalid_email_verification_code)

        return user

    def login_user(self, email: EmailStr, password: str) -> dict:
        user = (
            UserCore(self.db)
            .get_user_by_email(email=email, user_status=[Status.active, Status.passive], show_error=False)
        )

        if not user or not self.hash_helper.verify_password(user.password_hash, password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=errors.user_not_found)

        if user.status != Status.active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.inactive_user)

        access_token = create_access_token({"email": user.email})

        self.db.add(user)
        self.db.commit()

        return {"access_token": access_token, "token_type": "bearer"}

    def verify_email(self, email: EmailStr, code: str) -> dict:
        user = self._verify_code_and_exp_time(email=email, code=code)
        return UserCore(self.db).verify_email(user)

    def send_password_reset_mail(self, email: EmailStr) -> dict:
        user = UserCore(self.db).get_user_by_email(email=email)

        email_verification_code = UserCore(self.db)._generate_verification_code()  # noqa
        user.email_verification_code = email_verification_code
        user.email_verification_code_exp_date = datetime.now() + timedelta(seconds=settings.EMAIL_VERIFICATION_EXP_TIME)

        self.db.commit()

        send_template_mail(
            template_path="password_reset_mail.html",
            template_vars={"code": email_verification_code},
            subject="Şifre Sıfırlama Maili",
            receivers=user.email,
        )

        return {"message": "Şifre sıfırlama maili başarıyla gönderildi."}

    def user_password_reset(self, email: EmailStr, code: str, new_password: str) -> dict:
        user = self._verify_code_and_exp_time(email=email, code=code)
        UserCore(self.db).reset_user_password(user=user, new_password=new_password)

        return {"message": "Parola başarıyla güncellendi."}
