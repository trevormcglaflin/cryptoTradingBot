"""
The purpose of this is to conduct an analysis of the profitability of trades
taking into account the relative coinbase trading fees.

https://help.coinbase.com/en/pro/trading-and-funding/trading-rules-and-fees/fees
the link above contains information about fees on coinbase. Pretty much it classifies
trades into two categories: makers and takers. Takers are market orders, and makers
are limit orders.

For each type of trade, there are specific fees based on your trading volume in the
prior 30 days. The higher your trading volume, the lower the fees which is good for us.
For our purposes, we will likely have a trading volume between 100,000 and 20,000,000 for
a given month so I'm going to just use a flat maker and taker rate for those volume ranges.
We will use 0.2% as our rate for market orders and 0.1% as our rate for maker orders. In realitu,
it may be a little lower or higher than this, but that is roughly what it will fall into

NOTE: these rates apply for buys and sells. So if you bought $1000 at market, we will have a
$1,000 * 0.2% fee which is $2. If we sold $1,000 at market, we will again have a $2 fee. So the
combined fee for buying and selling is (buy price * fee rate) + (sell price * fee rate)

"""

import csv

TAKER_FEE = 0.002
MAKER_FEE = 0.001

def main():
    buy_price = 1000
    sell_price = 1000
    with open('selling_prices.csv', mode='w') as selling_prices:
        selling_price_writer = csv.writer(selling_prices, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # write header
        selling_price_writer.writerow(['Buy Price', 'Percent Gain', 'Sell Price'])

        # loop through buy prices in 100 dollar increments 100-10000
        for buy_price in range(100, 10000, 100):
            selling_price_writer.writerow([buy_price, 0, calculate_break_even_selling_price(buy_price)])
            for percent_gain in range(5, 500, 5):
                selling_price_writer.writerow([buy_price, percent_gain/1000, calculate_selling_price_for_percent_gain(buy_price, percent_gain/1000)])







def calculate_dollar_return(buy_price, sell_price, is_market_order=True):
    no_fee_return = sell_price - buy_price
    if is_market_order:
        fee = (buy_price * TAKER_FEE) + (sell_price * TAKER_FEE)
    else:
        fee = (buy_price * MAKER_FEE) + (sell_price * MAKER_FEE)
    return no_fee_return - fee

# params: buy price (float), is_market_order (bool)
# return: sell price to break even with fees
def calculate_break_even_selling_price(buy_price, is_market_order=True):
    if is_market_order:
        return ((TAKER_FEE * buy_price) + buy_price)/(1 - TAKER_FEE)
    else:
        return ((MAKER_FEE * buy_price) + buy_price) / (1 - MAKER_FEE)

# params: buy price (float), target_percent_gain (float), is_market_order (bool)
# returns: sell price to reach that percent gain with fees
def calculate_selling_price_for_percent_gain(buy_price, target_percent_gain, is_market_order=True):
    dollars_to_hit_gain = buy_price * target_percent_gain
    if is_market_order:
        return ((TAKER_FEE * buy_price) + buy_price + dollars_to_hit_gain)/(1 - TAKER_FEE)
    else:
        return ((MAKER_FEE * buy_price) + buy_price + dollars_to_hit_gain)/(1 - MAKER_FEE)



main()



