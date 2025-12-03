from fastapi import FastAPI
from schemas import EmailSchema
from kafka_producer import send_email_event

app = FastAPI()

@app.post("/send-email")
def send_email(payload: EmailSchema):
    data = payload.dict()
    send_email_event(data)
    return {"status": "queued", "data": data}
