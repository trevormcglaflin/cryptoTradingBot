from coinbase.wallet.client import Client
from time import sleep
from constants import api_key, api_secret
import constants
import cbpro
import pandas as pd


# useful links
#https://developers.coinbase.com/docs/wallet/guides/buy-sell
#https://algotrading101.com/learn/coinbase-api-guide/
# https://pypi.org/project/cbpro/

# NOTE: in cbpro, there are two types of "clients"
# 1. PublicClient: doesn't require any API passwords, lets you get historical price data
# 2. AuthenticatedClient: requires an API public key, secret key and passphrase, used to actually execute buys and sells and get any account information

# PUBLIC CLIENT METHODS

# to create a public client
public_client = cbpro.PublicClient()

# get products
# this function pretty much just gets general information about different cryptos like their ticker, base currency,
# quote currency, minimum order sizes, and other order limitations
# the return type is a 2d list or something like that
products = public_client.get_products()


# gets the "order book" for a particular crypto
# not really sure how to use this too well but it pretty much gives current bid and ask volumes for each number
# so if we were to use a volume strategy it would probably be useful
order_book = public_client.get_product_order_book('BTC-USD')

# this function will return a snapshot of information about a particular crypto including current price, current bids,
# current asks, and volume. Once again not too sure how to use the volume info but i think we can call it to get
# the current price which is useful. The return type is a dictionary
ticker = public_client.get_product_ticker(product_id='ETH-USD')

# this is a live stream of all trades for a particular crytpo
# in other words, everytime a trade is executed it will show the timestamp, tradeid, price in USD, size, and side
# it returns a generator which you cannot index directly, you can iterate over it by using a for loop though
trades = public_client.get_product_trades(product_id='ETH-USD')
#for trade in trades:
    #print(trade)



# this is how we get the "candlestick" info
# so for each block we can see the [timestamp, low_price, high_price, open_price, close_price, trading_volume]
# NOTE: the timestamps are in a funky time format which is standardized across all time zones.
hist_rates = public_client.get_product_historic_rates('ETH-USD')
print(hist_rates)

