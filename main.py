import requests
import datetime as dt
from twilio.rest import Client
import os

STOCK = input("What is the company stock name?")
COMPANY_NAME = input("What is the company name?")

STOCK_ENDPOINT = os.environ.get("STOCK_ENDPOINT")
NEWS_ENDPOINT = os.environ.get("NEWS_ENDPOINT")

stock_api_key = os.environ.get("STOCK_API_KEY")
news_api_key = os.environ.get("NEWS_API_KEY")

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

date = dt.datetime.now().date()
yesterday = date - dt.timedelta(1)
yesterday_2 = date - dt.timedelta(2)

yesterday_date = yesterday.strftime('%Y-%m-%d')
yesterday_2_date = yesterday_2.strftime('%Y-%m-%d')

stock_parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key
}

news_parameter = {
    "q": COMPANY_NAME,
    "from": yesterday_2_date,
    "to": date,
    "searchIn": "title,content",
    "language": "en",
    "apiKey": news_api_key
}


stock_reponse = requests.get(url=STOCK_ENDPOINT, params=stock_parameter)
stock_reponse.raise_for_status()

stock_data = stock_reponse.json()
print(stock_data)
daily_stock = stock_data["Time Series (Daily)"]
yesterday_closing_stock = daily_stock[yesterday_date]["4. close"]
the_day_before_yesterday_closing_stock = daily_stock[yesterday_2_date]["4. close"]

closing_stock = float(yesterday_closing_stock) - float(the_day_before_yesterday_closing_stock)
emoji = None
if closing_stock < 0:
    emoji = "🔻"
else:
    emoji = "🔺"
percentage_of_the_closing_stock = closing_stock / the_day_before_yesterday_closing_stock * 100
print(percentage_of_the_closing_stock)
if abs(percentage_of_the_closing_stock) > 0:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameter)
    news_response.raise_for_status()
    news_data = news_response.json()
    news_articles = news_data["articles"][0:3]

    news = [[x["title"], x["description"]] for x in news_articles]
    for x in news:
        client = Client(account_sid, auth_token)
        # noinspection PyTypeChecker
        message = client.messages \
            .create(
                body=f"{STOCK}{emoji}{abs(round(percentage_of_the_closing_stock))}%\n{x[0]}\n {x[1]}",
                from_='+12185173808',
                to='+2349014042165'
            )

