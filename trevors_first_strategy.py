import cbpro
import websocket
import numpy as np
import pandas as pd
import cbpro, time
from constants import sandbox_api_passphrase, sandbox_api_public, sandbox_api_secret



# define global variables
auth_client = cbpro.AuthenticatedClient(sandbox_api_public, sandbox_api_secret, sandbox_api_passphrase,
                                            api_url="https://api-public.sandbox.pro.coinbase.com")
TRADE_SYMBOL = "BTC-USD"
prices = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
buy_prices = []
sell_prices = []
total_buys = 0
gains = 0
actual_gains = 0
TAKER_FEE = 0.002
MAKER_FEE = 0.001
PERCENT_TO_BUY = 0.15


# get the start portfolio balance in USD
accounts = auth_client.get_accounts()
for account in accounts:
    if account['currency'] == "USD":
        start_balance = account['balance']

class myWebsocketClient(cbpro.WebsocketClient):

    # called when we open the webSocketClient
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = "BTC-USD"
        self.channels = ["ticker"]  # ticker, heartbeat, level2
        print(TRADE_SYMBOL + " Trading Bot has begun!")
        print("Start Balance is $" + start_balance + " USD")

    # what to do for each row of data that is reserved to our client from the websocket source (server)
    def on_message(self, msg):
        global prices, total_buys, gains, actual_gains
        try:
            prices.append(float(msg['price']))
            time.sleep(2)
            print("boom")
        except:
            pass

        # this will execute a buy and limit sell when the price reaches a trigger and there
        # is not already a limit order pending
        if self.get_buy_trigger_price(10) > prices[-1] and not self.limit_order_pending():
            print("Buy at " + str(prices[-1]))
            buy_prices.append(prices[-1])
            auth_client.buy(size=PERCENT_TO_BUY,
                            order_type='market',
                            product_id=TRADE_SYMBOL)

            print("Limit sell placed at " + str(buy_prices[-1] + 30))

            auth_client.sell(price=round(buy_prices[-1], 2) + 30,
                             size=PERCENT_TO_BUY,
                             order_type='limit',
                             product_id=TRADE_SYMBOL)
            total_buys += 1



    # TODO: update this function to buy at a good time
    def get_buy_trigger_price(self, time_span):
        last_x_prices = prices[-time_span:]
        last_x_prices.sort()
        return last_x_prices[2]

    # returns true if there is a limit order pending
    def limit_order_pending(self):
        orders = auth_client.get_orders()
        order_count = 0
        for order in orders:
            order_count += 1
        return order_count != 0

    # lets grab our results when we decide to close our websocket connection
    def on_close(self):
        print("ending...")


def main():
    # run the client

    # change this to determine how long you want to run the bot
    SECONDS_TO_RUN = 1000
    wsClient = myWebsocketClient()
    wsClient.start()
    second_count = 0
    while (second_count < SECONDS_TO_RUN):
        second_count += 1
        time.sleep(1)
    wsClient.close()

    # cancel any pending orders and covert all BTC back into USD
    if wsClient.limit_order_pending():
        auth_client.cancel_all()
        auth_client.sell(size=PERCENT_TO_BUY,
                         order_type='market',
                         product_id="BTC-USD")

    # get the end portfolio balance in USD
    accounts2 = auth_client.get_accounts()
    for account2 in accounts:
        if account2['currency'] == "USD":
            end_balance = account2['balance']

    print("Start Balance $", start_balance)
    print("End Balance $", end_balance)



if __name__ == '__main__':
    main()


