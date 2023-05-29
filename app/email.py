from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from .config import settings


conf = ConnectionConfig(
    MAIL_USERNAME =settings.mail_username,
    MAIL_PASSWORD = settings.mail_password,
    MAIL_FROM = settings.mail_from,
    MAIL_PORT = settings.mail_port,
    MAIL_SERVER = settings.mail_server,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER="app/templates"
    )


async def send_registration_email(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html'
    )

    fm = FastMail(conf)
    await fm.send_message(message=message, template_name='email_template.html')