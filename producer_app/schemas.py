from pydantic import BaseModel
from typing import Optional, Dict

class EmailSchema(BaseModel):
    email_to: str
    subject: str
    body: Optional[str] = None  # plain body fallback
    template: Optional[str] = None  # e.g. "welcome.hbs"
    data: Optional[Dict] = None  # variables for the template
