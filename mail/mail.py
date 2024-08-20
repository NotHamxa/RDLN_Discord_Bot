import asyncio
from fastapi_mail import FastMail,MessageSchema,ConnectionConfig

from models.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mailUsername,
    MAIL_PASSWORD=settings.mailPassword,
    MAIL_FROM=settings.mailUsername,
    MAIL_PORT=settings.mailPort,
    MAIL_SERVER=settings.mailServer,
    MAIL_FROM_NAME=settings.mailFromName,
    MAIL_STARTTLS=settings.mailStartTLS,
    MAIL_SSL_TLS=settings.mailSSLTLS,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="models/emailTemp"
)

def sendVerificationMail(subject, email_to, body) -> None:
    asyncio.run(sendVerificationWrapperFunc(subject, email_to, body))


async def sendVerificationWrapperFunc(subject, email_to, body):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message=message, template_name="verificationMailTemp.html")

