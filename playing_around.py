import cbpro
import os
import ta
import websocket
import pprint
import numpy as np
import pandas as pd
import cbpro, time
from constants import sandbox_api_passphrase, sandbox_api_public, sandbox_api_secret

print(sandbox_api_passphrase)
print(sandbox_api_public)
print(sandbox_api_secret)
auth_client = cbpro.AuthenticatedClient(sandbox_api_public, sandbox_api_secret, sandbox_api_passphrase,
                                        api_url="https://api-public.sandbox.pro.coinbase.com")
#accounts = auth_client.get_accounts()
#for account in accounts:
    #print(account)


auth_client.buy(size='0.05',  # BTC
                order_type='market',
                product_id="BTC-USD")






