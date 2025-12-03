import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load .env from root folder
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))   # go one level up
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_email(email_to: str, subject: str, body: str):
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise Exception("SMTP_EMAIL or SMTP_PASSWORD missing in .env")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = email_to

    # Use SSL (recommended by Google)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, [email_to], msg.as_string())

    print(f"📧 Email sent to {email_to}")
