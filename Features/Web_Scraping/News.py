import random
import requests
from googletrans import Translator


def ToEnglish(audio):
    if len(audio) > 3:
        Translate = Translator()
        Sent = Translate.translate(audio)
        text = Sent.text
        return text
    elif "None" in audio:
        print("Could not Understand")
    else:
        pass


def latest_news():
    country = ['us', 'in', 'cn', 'ru', 'jp', 'fr', 'sg']
    cn = random.choice(country)
    news_headlines = []
    news_Des = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country={cn}&apiKey=587dcad64761431490f655fda8c69018&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
        news_Des.append((article["description"]))
        news_Des = ToEnglish(str(news_Des))
        news_headlines = ToEnglish(str(news_headlines))
        news_Des = news_Des.replace("[", "").replace("]", "").replace("'", "")
        news_headlines = news_headlines.replace("[", "").replace("]", "").replace("'", "")
        News = f"Sir! Here are the latest news headlines:\n{news_headlines} \nUpdate of the News: {news_Des}"
        return News




