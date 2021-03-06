import requests     #API
#import re           # regex
import os           # environment variables for secrets
import numpy
from telegram import Bot as telegramBot
from telegram import ParseMode as telegramParseMode

# TODO: Add notice of the APIs used.

# Bitstamp=https://www.bitstamp.net/api/, Blockchain=https://blockchain.info/api/exchange_rates_api, Coindesk=http://www.coindesk.com/api/, https://localbitcoins.net/api-docs/
bitcoinApiEndpoints = \
{
    "Bitstamp": {"USD": "https://www.bitstamp.net/api/v2/ticker/btcusd/", "EUR": "https://www.bitstamp.net/api/v2/ticker/btceur/"},
    "Blockchain": "https://blockchain.info/ticker",
    "Coinbase": "https://api.coinbase.com/v2/exchange-rates?currency=BTC",
    "Coindesk": "http://api.coindesk.com/v1/bpi/currentprice.json",
    "Localbitcoins": "https://localbitcoins.net/bitcoinaverage/ticker-all-currencies/"
}
# The block below creates a hash and inserts values retrieved from multiple APIs.
# TODO: Catch exceptions instead of failing abruptly.
bitcoinCurrentPrice = {"USD": {}, "EUR": {}}
bitcoinCurrentPrice["USD"]["Bitstamp"] = requests.get(bitcoinApiEndpoints["Bitstamp"]["USD"]).json()["last"]
bitcoinCurrentPrice["EUR"]["Bitstamp"] = requests.get(bitcoinApiEndpoints["Bitstamp"]["EUR"]).json()["last"]
bitcoinCurrentPrice["USD"]["Blockchain"] = requests.get(bitcoinApiEndpoints["Blockchain"]).json()["USD"]["last"]
bitcoinCurrentPrice["EUR"]["Blockchain"] = requests.get(bitcoinApiEndpoints["Blockchain"]).json()["EUR"]["last"]
bitcoinCurrentPrice["USD"]["Coinbase"] = requests.get(bitcoinApiEndpoints["Coinbase"]).json()["data"]["rates"]["USD"]
bitcoinCurrentPrice["EUR"]["Coinbase"] = requests.get(bitcoinApiEndpoints["Coinbase"]).json()["data"]["rates"]["EUR"]
bitcoinCurrentPrice["USD"]["Coindesk"] = requests.get(bitcoinApiEndpoints["Coindesk"]).json()["bpi"]["USD"]["rate"].replace(",", "")
bitcoinCurrentPrice["EUR"]["Coindesk"] = requests.get(bitcoinApiEndpoints["Coindesk"]).json()["bpi"]["EUR"]["rate"].replace(",", "")
bitcoinCurrentPrice["USD"]["Localbitcoins"] = requests.get(bitcoinApiEndpoints["Localbitcoins"]).json()["USD"]["avg_1h"]
bitcoinCurrentPrice["EUR"]["Localbitcoins"] = requests.get(bitcoinApiEndpoints["Localbitcoins"]).json()["EUR"]["avg_1h"]

bitcoinCurrentAveragePrice = {"USD": 0, "EUR": 0} # Initialising the hash of average prices.
bitcoinCurrentPriceList = {"USD": [], "EUR": []} # This list contains two arrays with the prices for USD and EUR.

# The block below inserts the prices gathered in bitcoinCurrentPrice hash into bitcoinCurrentPriceList.
for currency, currencyProviders in bitcoinCurrentPrice.items():
    for provider, price in bitcoinCurrentPrice[currency].items():
        bitcoinCurrentPrice[currency][provider] = float(price)
        bitcoinCurrentPriceList[currency].append(float(price))

for currency, currencyList in bitcoinCurrentPriceList.items():
    bitcoinCurrentAveragePrice[currency] = numpy.median(bitcoinCurrentPriceList[currency])

# Database


# Telegram
## TOKENS
telegramToken = os.environ["telegramToken"]         # Bot token
telegramAdminId = os.environ["telegramAdminId"]     # The administrator of this bot
telegramChatId = os.environ["telegramChatId"]
# TODO: Allow reading an array of telegramChatIds to deliver updates to multiple chats.
##MESSAGE FORMATTING
telegramText = "Currently, 1 #Bitcoin #XBT equals:" + "\n" + "`" + str(bitcoinCurrentAveragePrice["EUR"]) + "` #EUR" + "\n" + "`" + str(bitcoinCurrentAveragePrice["USD"]) + "` #USD" + "\n" + "#ExchangeRates"
##DELIVERY
telegramBitcoin = telegramBot(token=telegramToken)
telegramBitcoin.send_message(chat_id=telegramChatId, text=telegramText, parse_mode=telegramParseMode.MARKDOWN, disable_web_page_preview=True)
