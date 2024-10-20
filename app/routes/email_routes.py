from fastapi import APIRouter, BackgroundTasks
from pydantic import EmailStr, BaseModel
from app.utils.email_utils import send_email

email_routes = APIRouter()

class EmailSchema(BaseModel):
    subject: str
    recipients: list[EmailStr]
    body: str

@email_routes.post("/send-email")
async def send_email_route(email: EmailSchema, background_tasks: BackgroundTasks):
    test = await send_email(email.subject, email.recipients, email.body)

    if test is True:
        return {"message": "Email sending task has been send"}
    else:
        return {"message": "Email sending task has been failed"}
