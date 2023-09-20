import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SENDER_EMAIL = os.getenv("MY_EMAIL")
RECEIVER_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("MY_EMAIL_PASSWORD")

HOST = "smtp.gmail.com"
PORT = 465

SUBJECT = "Daily Internship News"

msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg["Subject"] = SUBJECT

context = ssl.create_default_context()


def send_email(email_message):
    """Sends an email."""
    msg.attach(MIMEText(email_message, "html"))
    with smtplib.SMTP_SSL(host=HOST, port=PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg=msg.as_string())
