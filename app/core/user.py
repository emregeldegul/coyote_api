from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

from app.helpers.email_helper import send_template_mail
from app.helpers.error_helper import ErrorCode as errors
from app.helpers.hash_helper import HashHelper
from app.helpers.string_helper import generate_verification_code
from app.models.enums import Status
from app.models.user import User
from settings import settings


class UserCore:
    def __init__(self, db):
        self.db = db
        self.hash_helper = HashHelper()

    # Base Functions
    @staticmethod
    def _generate_verification_code():
        if settings.DEVELOPER_MODE:
            email_verification_code = settings.DEVELOPER_MODE_TEST_CODE
        else:
            email_verification_code = generate_verification_code(length=settings.VERIFICATION_CODE_LENGTH)

        return email_verification_code

    def get_user_by_email(self, email: EmailStr, user_status=None, show_error: bool = True) -> User:
        """
        This function checks for the existence of a user with the given email address
        :param email: E-mail address to check
        :param user_status: Allows searching by user's status (default: Active)
        :param show_error: Specifies whether to give an error when the user is not found. If given false, the empty object is returned
        :return: User Object
        """
        if user_status is None:
            user_status = [Status.active]

        user = self.db.query(User).filter(User.email == email, User.status.in_(user_status)).first()

        if not user and show_error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors.user_not_found)

        return user

    def get_user_by_id(self, user_id: int, user_status=None, show_error: bool = True) -> User:
        if user_status is None:
            user_status = [Status.active]

        user = self.db.query(User).filter(User.id == user_id, User.status.in_(user_status)).first()

        if not user and show_error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors.user_not_found)

        return user

    # CURD Functions
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: EmailStr,
        password: str,
        email_verification: bool = False,
        user_status: Status = Status.active,
    ) -> dict:
        user = self.get_user_by_email(email, show_error=False)

        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.user_already_exists)

        email_verification_code = self._generate_verification_code()

        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.email_verification = email_verification
        user.email_verification_code = email_verification_code
        user.email_verification_code_exp_date = datetime.now() + timedelta(
            seconds=settings.EMAIL_VERIFICATION_EXP_TIME  # type: ignore
        )
        user.password_hash = self.hash_helper.get_password_hash(password)
        user.status = user_status

        self.db.add(user)
        self.db.commit()

        if not email_verification:
            send_template_mail(
                template_path="account_active_mail.html",
                template_vars={"code": email_verification_code},
                subject="Aktivasyion Maili",
                receivers=user.email,
            )
        return {"message": "Kullanıcı başarıyla oluşuruldu."}

    @staticmethod
    def get_user_detail(user: User):
        return jsonable_encoder(user)

    def verify_email(self, user: User) -> dict:
        user.email_verification = True
        user.email_verification_date = datetime.now()
        self.db.commit()

        return {"message": "Kullanıcı e-posta adresi doğrulandı."}

    def reset_user_password(self, user: User, new_password: str) -> dict:
        user.password_hash = self.hash_helper.get_password_hash(new_password)
        self.db.commit()

        return {"message": "Kullanıcı şifresi güncelledi."}
