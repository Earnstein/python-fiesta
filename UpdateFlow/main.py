import os
import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# API essentials
API_KEY = os.getenv("NEWS_ORG_API_KEY")
ENDPOINT = "https://newsapi.org/v2/everything"

header = {
    "X-Api-Key": API_KEY
}

# Email setup
HOST = "smtp.gmail.com"
PORT = 465
PASSWORD = os.getenv("MY_EMAIL_PASSWORD")

# Email parameters

SENDER_EMAIL = os.getenv("MY_EMAIL")
RECEIVER_EMAIL = os.getenv("MY_EMAIL")
subject = "Daily Internship news"


def send_email(message):
    """sends an email"""

    # Email constructor
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    context = ssl.create_default_context()
    msg.attach(MIMEText(message, "plain"))
    with smtplib.SMTP_SSL(host=HOST, port=PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg=msg.as_string())


def get_news(date):
    """Gets the five most recent internship news from news_org"""
    params = {
        "q": "internships",
        "date": date
    }
    request = requests.get(url=ENDPOINT, headers=header, params=params)
    request.raise_for_status()
    response = request.json()
    news_list = (response["articles"][:5])
    return news_list


articles = get_news(date="2023-08-01")
news_result = [{"title": article["title"], "url": article["url"], "description": article["description"]} for article in
               articles]
print(news_result)
