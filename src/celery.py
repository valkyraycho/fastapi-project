from asgiref.sync import async_to_sync
from fastapi_mail import MessageSchema, MessageType
from pydantic import EmailStr

from celery import Celery

from .email import fm

app = Celery()

app.config_from_object("src.config")


@app.task()
def send_email(recipients: list[EmailStr], subject: str, body: str) -> None:
    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )
    async_to_sync(fm.send_message)(message)
