from confluent_kafka import Consumer
import json
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.text import MIMEText

# ------------------------
# Jinja Environment
# ------------------------
env = Environment(loader=FileSystemLoader("consumer_app/templates"))

# ------------------------
# Kafka Consumer Setup
# ------------------------
conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "email-service",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)
consumer.subscribe(["EMAIL"])

print("📩 Email consumer started...")

# ------------------------
# Send Email Function
# ------------------------
def send_email(to, subject, html):
    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"] = "yourgmail@gmail.com"
    msg["To"] = to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("yourgmail@gmail.com", "your_app_password")
        smtp.send_message(msg)

    print(f"✅ Email sent to {to}")

# ------------------------
# Main Consumer Loop
# ------------------------
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print("⚠️ Consumer error:", msg.error())
        continue

    try:
        payload = json.loads(msg.value().decode("utf-8"))
        print("📩 Received event:", payload)

        template_name = payload["template"] + ".hbs"

        template = env.get_template(template_name)   # load template
        html = template.render(payload["data"])      # apply variables

        send_email(
            payload["email_to"],
            payload["subject"],
            html
        )

    except Exception as e:
        print("❌ Error processing message:", str(e))
