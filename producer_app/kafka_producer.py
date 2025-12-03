from confluent_kafka import Producer
import json

producer = Producer({"bootstrap.servers": "localhost:9092"})

def send_email_event(data: dict):
    """
    Produces an email event to the EMAIL Kafka topic.
    """
    producer.produce("EMAIL", json.dumps(data).encode("utf-8"))
    producer.flush()
    print("📤 Email event produced successfully!")
