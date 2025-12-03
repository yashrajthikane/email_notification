import smtplib
from email.mime.text import MIMEText
import os
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

# Load environment variables from root .env
load_dotenv()

EMAIL = os.getenv("SMTP_EMAIL")
PASSWORD = os.getenv("SMTP_PASSWORD")

# Build absolute path to templates/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# Initialize Jinja2 environment using ABSOLUTE path
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def send_email(email_to: str, subject: str, body: str):
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = email_to

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [email_to], msg.as_string())

    print(f"📨 Plain email sent to {email_to}")


def send_templated_email(email_to: str, subject: str, template_name: str, data: dict):

    # Auto–add .hbs if user passes only name
    if not template_name.endswith(".hbs"):
        template_name += ".hbs"

    # Load template
    try:
        template = env.get_template(template_name)
    except Exception as e:
        raise FileNotFoundError(
            f"❌ Template '{template_name}' not found in {TEMPLATE_DIR}"
        )

    # Render HTML content
    html_content = template.render(**data)

    msg = MIMEText(html_content, "html")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = email_to

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [email_to], msg.as_string())

    print(f"📨 HTML template email sent to {email_to}")
