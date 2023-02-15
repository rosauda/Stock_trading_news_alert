import requests
import os
import datetime as date

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
print(stock_last_refreshed)

# Extract open and close price
stock_open = float(stock_data["Time Series (Daily)"][stock_last_refreshed]['1. open'])
stock_close = float(stock_data["Time Series (Daily)"][stock_last_refreshed]['4. close'])

# Check price variance
price_change = round(abs((stock_close/stock_open - 1) * 100), 2)

# ---------------------------- GETTING STOCK NEWS ------------------------------- #

get_news = False
if price_change > 5:
    get_news = True

response = requests.get(NEWS_ENDPOINT, params=parameters_news)

# Raising errors and exceptions
response.raise_for_status()

# Data to json
stock_news = response.json()
stock_news = stock_news["data"][0]['entities'][0]['highlights']
print(stock_news)
print(len(stock_news))

for items in range(0, len(stock_news)):
    print(stock_news[items]['highlight'])


## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file 
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file 
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
"""

