from coinbase.wallet.client import Client
from time import sleep
from constants import sandbox_api_passphrase, sandbox_api_public, sandbox_api_secret
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
# NOTE: the timestamps are in a funky time format which is standardized across all time zones. its called epoch
# https://www.epochconverter.com/ this link helps you convert normal time to epoch. Keep in mind it is not in our time zone
# you can choose how "granular" the candlesticks are, aka how long of a time each candle represents
# The granularity field must be one of the following values: {60, 300, 900, 3600, 21600, 86400} in seconds
# 60 = 1 minute, 300 = 5 minutes, 900 = 15 minutes, 3600 = 1 hour, 21600 = 6 hours, 86400 = 24 hours
# the 0 index represents the most recent 5 minutes, then it goes backwards in time for 300 blocks
hist_rates = public_client.get_product_historic_rates('ETH-USD')


# this just gets the last 24 hour stats for a particular crypto
# its a dictionary including { open, high, low, volume, last, volume30day }
# not going to be super useful because we got the historic rates above
stats_24_hours = public_client.get_product_24hr_stats('ETH-USD')

# this just returns some general information about each crypto like ticker symbol, name, sign, precision, etc
# not super useful
currencies = public_client.get_currencies()


# this returns time in normal time format and epoch (which is the funky time)
# it will actually be useful to have the epoch time
time = public_client.get_time()

# AUTHENTICATED CLIENT METHODS

# to create an authenticated client
#auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

# to create an authenticated client in sandbox
auth_client = cbpro.AuthenticatedClient(sandbox_api_public, sandbox_api_secret, sandbox_api_passphrase,
                                        api_url="https://api-public.sandbox.pro.coinbase.com")


# get accounts: returns a list of dictionaries about all of your different wallets
# each account has the following attributes: id, currency (ie BTC), balance, hold, available, profile_id, trading enabled (bool)
accounts = auth_client.get_accounts()


# you can also get a single account by passing in the id for the account
# this returns a single dictionary
single_account = auth_client.get_account("c1b360c4-8b21-414a-83a9-30a067c2bafa")

# to search for an account you could do a for loop, this is how i would search for my BTC wallet
for account in accounts:
    if account['currency'] == "BTC":
        bitcoin_id = account['id']


# this returns trading history for a particular account
# it returns a generator object which is kind of weird to use
account_history = auth_client.get_account_history(bitcoin_id)

# returns all account holds as a generator object
account_holds = auth_client.get_account_holds(bitcoin_id)

# PLACING ORDERS

# limit orders

# limit buy (two ways)
# the "price" parameter means that the buy will execute if the price goes below that amount
# the "size" parameter represents the amount of the currency that will be purchased so here it will be 0.01 * 35000ish which is like 350
#auth_client.buy(price='50000',
               #size="500",
               #order_type='limit',
               #product_id='BTC-USD')
# OR
#auth_client.place_limit_order(product_id='BTC-USD',
                              #side='buy',
                              #price='50000',
                              #size='0.05')


# limit sell (two ways)
# the "price" is the price that needs to be reached for the sell to be executed
# the "size" is the amount that will be sold in the non-USD currency
#auth_client.sell(price='50000', #USD
                #size='0.05', #BTC
                #order_type='limit',
                #product_id='BTC-USD')
# OR
#auth_client.place_limit_order(product_id='BTC-USD',
                              #side='sell',
                              #price='200.00',
                              #size='0.02')

# market orders

# market buy (two ways)
#auth_client.buy(size='0.05',  # BTC
                  #order_type='market',
                  #product_id="BTC-USD")
# OR
# you could also specify 'size' which is the amount of bitcoin you would buy
# funds represents the amount in USD
#auth_client.place_market_order(product_id='BTC-USD',
                               #side='buy',
                               #funds='1000.00')


# market sell (two ways)
#auth_client.sell(size='0.05',  # BTC
                #order_type='market',
                #product_id="BTC-USD")
# OR
#auth_client.place_market_order(product_id='BTC-USD',
                               #side='sell',
                               #funds='100.00')





