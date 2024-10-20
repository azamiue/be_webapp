from fastapi_mail import FastMail, MessageSchema, MessageType
from app.config.email_config import conf

async def send_email(subject: str, recipients: list, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        print("Test email sent successfully")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False