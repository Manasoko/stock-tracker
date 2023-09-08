import requests
import datetime as dt
from twilio.rest import Client

STOCK = input("What is the company stock name?")
COMPANY_NAME = input("What is the company name?")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_key = "XAVOCX21BEUO53KM"
news_api_key = "ff2c90901b3940f49ae3893af56cb35b"

account_sid = "AC45a32ff30a95710c640d9ca1aadb7f29"
auth_token = "fa7fe0946d50f5fe7c9fa98023ec0b36"

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

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the daily_stock before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the daily_stock before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
# HINT 2: Work out the value of 5% of yerstday's closing stock price.
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
    ## STEP 2: Use https://newsapi.org/docs/endpoints/everything
    # Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
    # HINT 1: Think about using the Python Slice Operator
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameter)
    news_response.raise_for_status()
    news_data = news_response.json()
    news_articles = news_data["articles"][0:3]

    ## STEP 3: se twilio.com/docs/sms/quickstart/python
    # Send a separate message with each article's title and description to your phone number.
    # HINT 1: Consider using a List Comprehension.
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

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
