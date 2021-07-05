Crypto Trading Bot
Collaborators: Trevor McGlaflin and Qin Quan Lin

The Goal 
The goal of this project is to create a crypto trading bot that places
automatic buy and sell orders through coinbase API. It will be a very short
term trading strategy that uses candlesticks and volumes, as well as trend
indicators like 20MA and RSI to signal good times to place orders. 

To run:
1. create a coinbase api sandbox account (https://public.sandbox.pro.coinbase.com/)
2. generate API keys by clicking your name in upper right corner -> API -> add new API key
3. create a constants.py file that will store the public key, secret key and passphrase
4. use these credentials to create an authenticated client
5. run the script `python3 trading_bot.py`
