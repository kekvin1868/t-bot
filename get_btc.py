import ccxt
import os
from datetime import datetime

# CCXT is an open-source toolkit (Python, JavaScript/TypeScript, PHP, C#, Go) 
# Lets you talk to 100-plus crypto exchanges.

# TKO object
exchange = ccxt.tokocrypto({
  'apiKey': os.environ.get('TKCR_API_KEY'),
  'secret': os.environ.get('TKCR_PRV_KEY'),
  'enableRateLimit': True, # Prevents API hit limit
})

# Trade symbol, currently set to just 1
symbol = 'BTC/USDT'

def fetch_ohlcv_data(exchange, symbol, timeframe='1h', limit=100):
  """
  Fetches historical candlestick (OHLCV) data for a given symbol & timeframe.
  """
  try:
    print(f"Fetching historical OHLCV data for {symbol} ({timeframe})...")
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

    if ohlcv:
      print(f"Successfully fetched {len(ohlcv)} {timeframe} candles for {symbol}.")
      print("--- Example of last 5 candles (Timestamp, Open, High, Low, Close, Volume) ---")
      for candle in ohlcv[-5:]:
          # Convert timestamp from milliseconds to a human-readable datetime
          timestamp_dt = datetime.fromtimestamp(candle[0] / 1000)
          print(f"{timestamp_dt}: O={candle[1]}, H={candle[2]}, L={candle[3]}, C={candle[4]}, V={candle[5]:,.2f}") # Added formatting for Volume
      print("-" * 30)
    else:
      print(f"Failed to fetch historical OHLCV data for {symbol}.")

  except ccxt.ExchangeError as e:
      print(f"Error connecting to Tokocrypto or fetching OHLCV data: {e}")
      print("Please ensure your API keys are correct and have necessary permissions (read access).")
  except ccxt.NetworkError as e:
      print(f"Network error: {e}. Check your internet connection or VPN.")
  except Exception as e:
      print(f"An unexpected error occurred while fetching OHLCV: {e}")
    

def fetch_ticker_data(exchange, symbol):
  """
  Fetches current ticker for a given symbol.
  """
  try:
    print(f"Fetching ticker tape for {symbol} on Tokocrypto...")
    ticker = exchange.fetch_ticker(symbol)

    print("--- Current BTC/USDT Ticker ---")
    print(f"Symbol: {ticker['symbol']}")
    print(f"Last Price: {ticker['last']}")
    
    # Highest buy offer
    print(f"Bid Price: {ticker['bid']}")
    
    # Lowest sell offer
    print(f"Ask Price (lowest sell offer): {ticker['ask']}")
    
    # Total amount of BTC being traded in a day
    base_volume = ticker.get('baseVolume')

    # Fallback if failed to return or is empty.
    if(base_volume) is None or not isinstance(base_volume, (int, float)):
      base_volume = 0.0
    print(f"24h Volume (BTC): {ticker['baseVolume']:,.2f}")

    # Total amount of USDT being traded in a day
    quote_volume = ticker.get('quoteVolume')

    # Fallback if failed to return or is empty.
    if(quote_volume) is None or not isinstance(quote_volume, (int, float)):
      quote_volume = 0.0
    print(f"24h Volume (USDT): {ticker['quoteVolume']:,.2f}")

    print(f"Timestamp (UTC): {exchange.iso8601(ticker['timestamp'])}")

  except ccxt.ExchangeError as e:
    print(f"Error connecting to Tokocrypto or fetching data: {e}")
    print("Please ensure your API keys are correct and have necessary permissions (read access).")
  except ccxt.NetworkError as e:
    print(f"Network error: {e}. Check your internet connection.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
  fetch_ticker_data(exchange, symbol)

  ohlcv_timeframe = '1h'
  ohlc_num_candles = 200

  