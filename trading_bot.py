import cbpro
import os
import ta
import websocket
import pprint
import numpy as np
import pandas as pd
import cbpro, time
from constants import sandbox_api_passphrase, sandbox_api_public, sandbox_api_secret


# this primarily comes from
# https://medium.com/geekculture/how-to-build-an-rsi-crypto-bot-using-coinbase-pro-and-python-b7d462dbeaf4


# setup a public and authenticated client
public_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(sandbox_api_public, sandbox_api_secret, sandbox_api_passphrase,
                                        api_url="https://api-public.sandbox.pro.coinbase.com")

# coinbase setup
trade_symbol = "BTC-USD"
traded_quantity = .05
cbpro_fee = .005

# rsi setup
# these can be tweaked to change when we buy/sell
rsi_period = 14
rsi_overbought = 70
rsi_oversold = 30

# data storage setup
prices = []
open_position = False
total_buys = 0
total_sells = 0
order_book = {}
order_book['rsiBUY'] = []
order_book['priceBUY'] = []
order_book['priceSELL'] = []
order_book['rsiSELL'] = []
order_book['quantityPriceBUY'] = []
order_book['quantityPriceSELL'] = []
order_book['feeBUY'] = []
order_book['feeSELL'] = []


# inherited from the cbpro websocket client
# we must override these three methods for some reason
class myWebsocketClient(cbpro.WebsocketClient):

    # called when we open the webSocketClient
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = trade_symbol
        self.channels = ["ticker"]  # ticker, heartbeat, level2
        print(f"{trade_symbol} RSI Trading Bot has begun!")

    # what to do for each row of data that is reserved to our client from the websocket source (server)
    def on_message(self, msg):
        global prices, open_position, total_buys, total_sells
        try:
            # start trying to gather up the price data into an array.
            prices.append(float(msg['price']))
            # data interval (5min)
            # time.sleep(300)

        except:
            pass

        # Get enough data in our prices array to then start calculating RSI and trading on that calculation
        if len(prices) > rsi_period:
            np_prices = np.array(prices)
            ser = pd.Series(np_prices)
            rsi = ta.momentum.rsi(ser, rsi_period, False)
            last_rsi = rsi.iloc[-1]
            # print("Current Price: ", float(msg['price'])," | Current RSI: {}".format(last_rsi))

            # overbought trading order (sell high)
            if last_rsi > rsi_overbought:
                if open_position:
                    print("Overbought! SELL!")
                    order_book['rsiSELL'].append(last_rsi)
                    order_book['priceSELL'].append(float(msg['price']))
                    order_book['quantityPriceSELL'].append(float(msg['price']) * traded_quantity)
                    order_book['feeSELL'].append(float(msg['price']) * traded_quantity * cbpro_fee)
                    open_position = False
                    total_sells += 1
                    # TODO: actually place the sell order here
                    auth_client.sell(size='0.05',  # BTC
                                    order_type='market',
                                    product_id=trade_symbol)
                    print("Number of Sells: ", total_sells, " at an RSI of ", last_rsi)
                else:
                    pass
                    # print("You don't own anything.")

            # oversold trading order (buy low)
            if last_rsi < rsi_oversold:
                if open_position:
                    pass
                    # print("You already own it.")
                else:
                    print("Oversold! BUY!")
                    order_book['rsiBUY'].append(last_rsi)
                    order_book['priceBUY'].append(float(msg['price']))
                    order_book['quantityPriceBUY'].append(float(msg['price']) * traded_quantity)
                    order_book['feeBUY'].append(float(msg['price']) * traded_quantity * cbpro_fee)
                    open_position = True
                    total_buys += 1
                    # TODO: actually place the buy order here
                    auth_client.buy(size='0.05',  # BTC
                                    order_type='market',
                                    product_id=trade_symbol)
                    print("Number of Buys: ", total_buys, " at an RSI of ", last_rsi)

    # lets grab our results when we decide to close our websocket connection
    def on_close(self):
        print("------------ Results ------------\n")
        results = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in order_book.items()]))
        results['returnsBeforeFees'] = results.quantityPriceSELL - results.quantityPriceBUY
        results[
            'returnsAfterFees'] = results.quantityPriceSELL - results.quantityPriceBUY - results.feeBUY - results.feeSELL
        print('\n Total returns before Fees: ', results.returnsBeforeFees.sum())
        print('\n Total returns after Fees: ', results.returnsAfterFees.sum())
        # print(prices)


# this is where we actually call the websocket client
my_client = myWebsocketClient()
my_client.start()

