from fastapi_mail import FastMail, ConnectionConfig
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Get the project root directory
BASE_DIR = Path(__file__).parent.parent

email_conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_FROM = os.getenv('MAIL_FROM'),
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587)),
    MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,  # Add this for security
    TEMPLATE_FOLDER = BASE_DIR / 'email_templates'
)


fastmail = FastMail(email_conf)
