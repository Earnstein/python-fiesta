import os
import requests
from datetime import datetime
from backend import send_email

API_KEY = os.getenv("NEWS_ORG_API_KEY")
DATE = datetime.today().strftime("%Y-%m-%d")
ENDPOINT = "https://newsapi.org/v2/everything"
HEADER = {"X-Api-Key": API_KEY}


def get_news(topic: str, date, num_results=5):
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


def main():
    articles = get_news(topic="internships", date=DATE)
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

if __name__ == "__main__":
    main()