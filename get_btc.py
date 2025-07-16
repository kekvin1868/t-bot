import ccxt
import os

# CCXT is an open-source toolkit (Python, JavaScript/TypeScript, PHP, C#, Go) 
# Lets you talk to 100-plus crypto exchanges.

# TKO object
exchange = ccxt.tokocrypto({
  'apiKey': os.environ.get('TKCR_API_KEY'),
  'secret': os.environ.get('TKCR_PRV_KEY'),
  'enableRateLimit': True, # Prevents API hit limit
})

# Trade symbol, currently set to just 1
# TODO -> Multiple coins
symbol = 'BTC/USDT'

# TODO -> Bypass VPN, show more relevant data
try:
  print(f"Fetching ticker tape for {symbol} on Tokocrypto...")
  ticker = exchange.fetch_ticker(symbol)

  print("--- Current BTC/USDT Ticker ---")
  print(f"Symbol: {ticker['symbol']}")
  print(f"Last Price: {ticker['last']}")
  print(f"Bid Price (highest buy offer): {ticker['bid']}")
  print(f"Ask Price (lowest sell offer): {ticker['ask']}")
  print(f"24h Volume ({ticker['baseVolumeReference']}): {ticker['baseVolume']}") # Volume in BTC
  print(f"24h Volume ({ticker['quoteVolumeReference']}): {ticker['quoteVolume']}") # Volume in USDT
  print(f"Timestamp (UTC): {exchange.iso8601(ticker['timestamp'])}")

except ccxt.ExchangeError as e:
  print(f"Error connecting to Tokocrypto or fetching data: {e}")
  print("Please ensure your API keys are correct and have necessary permissions (read access).")
except ccxt.NetworkError as e:
  print(f"Network error: {e}. Check your internet connection.")
except Exception as e:
  print(f"An unexpected error occurred: {e}")