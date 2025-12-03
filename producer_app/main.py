from fastapi import FastAPI
from schemas import EmailSchema
from kafka_producer import send_email_event   # <-- FIX HERE

app = FastAPI()

@app.post("/send-email")
def send_email(payload: EmailSchema):
    event = payload.model_dump()   # convert to dict
    send_email_event(event)        # send to kafka
    return {"success": True, "message": "Email event pushed to Kafka"}
