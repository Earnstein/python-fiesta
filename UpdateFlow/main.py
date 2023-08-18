import os
import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


API_KEY = os.getenv("NEWS_ORG_API_KEY")
PASSWORD = os.getenv("MY_EMAIL_PASSWORD")
SENDER_EMAIL = os.getenv("MY_EMAIL")
RECEIVER_EMAIL = os.getenv("MY_EMAIL")

DATE = datetime.today().strftime("%Y-%m-%d")
ENDPOINT = "https://newsapi.org/v2/everything"
HEADER = {"X-Api-Key": API_KEY}
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


def get_news(topic: str, date=DATE, num_results=5):
    """Gets the specified number of most recent internship news from news_org"""
    params = {
        "q": topic,
        "date": date,
        "pageSize": num_results
    }
    request = requests.get(url=ENDPOINT, headers=HEADER, params=params)
    request.raise_for_status()
    response = request.json()
    news_list = (response["articles"])
    return news_list


articles = get_news(topic="internships", date="2023-08-01")
news_result = [
    {
        "title": article["title"],
        "url": article["url"],
        "description": article["description"]
    } for article in articles
]

messages = []
for news in news_result:
    title = news["title"]
    url = news["url"]
    description = news["description"]
    message = f"""
    <html>
        <body>
            <h2>HEADLINE: {title}</h2>
            <p>{description}</p>
            <p>Read more: <a href="{url}">{url}</a></p>
        </body>
    </html>
    """
    messages.append(message)

full_message = "\n".join(messages)
send_email(full_message)
