from confluent_kafka import Consumer
import json
from email_client import send_email

def main():
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "email-consumers",
        "auto.offset.reset": "earliest"
    }

    consumer = Consumer(consumer_config)
    consumer.subscribe(["EMAIL"])

    print("📥 Kafka Consumer started... Listening to EMAIL topic")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("❌ Error:", msg.error())
            continue

        try:
            payload = json.loads(msg.value().decode("utf-8"))
            print("📩 Received event:", payload)

            send_email(payload["email_to"], payload["subject"], payload["body"])

        except Exception as e:
            print("⚠️ Error processing message:", e)

if __name__ == "__main__":
    main()
