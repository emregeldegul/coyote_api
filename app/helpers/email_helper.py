import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, PackageLoader

from app.worker import celery_app
from settings import settings


@celery_app.task(name="send_email")
def send_mail(subject, receivers, body):
    if settings.DEVELOPER_MODE:
        return True

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.MAIL_USERNAME
        message["To"] = receivers

        part = MIMEText(body, "html")
        message.attach(part)

        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_SERVER_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(user=settings.MAIL_USERNAME, password=settings.MAIL_PASSWORD)
            server.sendmail(from_addr=settings.MAIL_USERNAME, to_addrs=receivers, msg=message.as_string())

            return True
    except Exception as e:  # noqa
        print(e)
        return False


def send_template_mail(template_path: str, template_vars: dict, subject: str, receivers: str):
    env = Environment(loader=PackageLoader("app", "templates/email"), autoescape=True)
    template = env.get_template(template_path)
    html = template.render(**template_vars)
    send_mail.delay(subject, receivers, html)

    return True
