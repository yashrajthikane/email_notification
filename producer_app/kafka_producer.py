from confluent_kafka import Producer
import json

producer = Producer({"bootstrap.servers": "localhost:9092"})

def send_email_event(data: dict):
    producer.produce("EMAIL", json.dumps(data).encode("utf-8"))
    producer.flush()
