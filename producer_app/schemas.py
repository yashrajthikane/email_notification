from pydantic import BaseModel

class EmailSchema(BaseModel):
    email_to: str
    subject: str
    body: str
