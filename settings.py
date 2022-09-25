from os import getenv, path

from dotenv import load_dotenv


class Settings:
    BASEDIR = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(BASEDIR, ".env"))

    # Base Settings
    SECRET_KEY = getenv("SECRET_KEY", "MercanBirSahildeymisGemilerBulmakKasvetliGunlereKaldi")
    EMAIL_VERIFICATION_EXP_TIME = getenv("EMAIL_VERIFICATION_EXP_TIME", 5 * 60)  # Minute
    VERIFICATION_CODE_LENGTH = getenv("VERIFICATION_CODE_LENGTH", 6)
    DEVELOPER_MODE = getenv("DEVELOPER_MODE", True)
    DEVELOPER_MODE_TEST_CODE = getenv("DEVELOPER_MODE_TEST_CODE", "123456")  # Length size -> "VERIFICATION_CODE_LENGTH"

    # APP and API Settings
    APP_VERSION = getenv("APP_VERSION", "v1")
    API_VERSION = getenv("API_VERSION", "0.0.1")
    APP_NAME = getenv("APP_NAME", "Coyote API")
    APP_URL = getenv("APP_URL", "http://0.0.0.0:8000/")
    API_URL = getenv("API_URL", "{app_url}{app_version}/".format(app_url=APP_URL, app_version=API_VERSION))
    APP_TIMEZONE = getenv("APP_TIMEZONE", "Europe/Istanbul")

    # Postgresql Database Settings
    POSTGRESQL_SERVER_NAME = getenv("POSTGRESQL_SERVER_NAME", "localhost")
    POSTGRESQL_SERVER_PORT = getenv("POSTGRESQL_SERVER_PORT", 5432)
    POSTGRESQL_USER_NAME = getenv("POSTGRESQL_USER_NAME", "postgres")
    POSTGRESQL_USER_PASSWORD = getenv("POSTGRESQL_USER_PASSWORD", "")
    POSTGRESQL_DATABASE_NAME = getenv("POSTGRESQL_DATABASE_NAME", "coyote")
    SQLALCHEMY_DATABASE_URI = getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://{user_name}:{user_password}@{server_name}:{server_port}/{database_name}".format(
            user_name=POSTGRESQL_USER_NAME,
            user_password=POSTGRESQL_USER_PASSWORD,
            server_name=POSTGRESQL_SERVER_NAME,
            server_port=POSTGRESQL_SERVER_PORT,
            database_name=POSTGRESQL_DATABASE_NAME,
        ),
    )

    # Redis Settings
    CELERY_BROKER_URL = getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # Mail Settings
    MAIL_SERVER = getenv("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_SERVER_PORT = getenv("MAIL_SERVER_PORT", 587)
    MAIL_USERNAME = getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD", "")

    # JWT Settings
    JWT_EXPIRES_TIME = getenv("JWT_EXPIRES_TIME", 60 * 24)  # Minute
    JWT_ALGORITHM = getenv("JWT_ALGORITHM", "HS256")

    # Author Settings
    AUTHOR_NAME = "Yunus Emre Geldegül"
    AUTHOR_URL = "https://emregeldegul.com.tr"
    AUTHOR_EMAIL = "yunusemregeldegul@gmail.com"


settings = Settings()
