import cbpro
import websocket
import numpy as np
import pandas as pd
import cbpro, time
from constants import sandbox_api_passphrase, sandbox_api_public, sandbox_api_secret


# information about TA-lib https://medium.com/analytics-vidhya/recognizing-over-50-candlestick-patterns-with-python-4f02a1822cb5
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

# https://www.ta-lib.org/
# https://www.youtube.com/watch?v=30BaSfz0FGE



# create auth client
public_client = cbpro.PublicClient()


hist_rates = public_client.get_product_historic_rates('BTC-USD', granularity=300)

print(hist_rates)