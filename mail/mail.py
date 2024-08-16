import asyncio
from fastapi_mail import FastMail,MessageSchema,ConnectionConfig

# from models.config import settings

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
    TEMPLATE_FOLDER="app/core/models/mailTemps"
)
