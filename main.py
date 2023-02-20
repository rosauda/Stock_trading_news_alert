import requests
import os
import datetime as date
import html

# ---------------------------- VARIABLES ------------------------------- #

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://api.marketaux.com/v1/news/all"

# Environment variables
api_key = os.environ["API_KEY"]
api_news_key = os.environ["API_NEWS_KEY"]

parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": api_key,
}

parameters_news = {
    "api_token": api_news_key,
    "symbols": STOCK,
}
# ---------------------------- GETTING CURRENT DATA USING API ------------------------------- #

response = requests.get(STOCK_ENDPOINT, params=parameters)

# Raising errors and exceptions
response.raise_for_status()

# Data to json
stock_data = response.json()

# Extract last day that the data was refreshed
stock_last_refreshed = stock_data["Meta Data"]["3. Last Refreshed"]

# Extract open and close price
stock_open = float(stock_data["Time Series (Daily)"][stock_last_refreshed]['1. open'])
stock_close = float(stock_data["Time Series (Daily)"][stock_last_refreshed]['4. close'])

# Check price variance
difference = round(abs(stock_close - stock_open))
variance = (difference / stock_close) * 100

# ---------------------------- GETTING STOCK NEWS ------------------------------- #

if variance > 1:

    # Get news
    response = requests.get(NEWS_ENDPOINT, params=parameters_news)
    # Raising errors and exceptions
    response.raise_for_status()
    # Data to json
    stock_news = response.json()["data"][0]['entities'][0]['highlights']
    print(stock_news)
    print(len(stock_news))

    new_list = [stock_news[news]['highlight'] for news in range(0, len(stock_news))]
    print(f"highlight:{new_list[0]}\nhighlight:{new_list[1]}")

else:
    print("Do not get news")



