from binance import Client
import pandas as pd
from tqdm import tqdm
from datetime import datetime


client = Client()

trading_symbols = client.get_exchange_info()['symbols']

kline_columns = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'NumberOfTrades',
           'TakerBuyBaseAssetVolume', 'TakerBuyQuoteASsetVolumne', 'Drop']


def get_trading_symbols(fiat='EUR'):
    return [symbol['symbol'] for symbol in trading_symbols if symbol['quoteAsset'] == fiat]


def get_klines(symbol, interval=Client.KLINE_INTERVAL_1DAY, start='1 Jan, 2018', **kwargs):
    raw_data = client.get_historical_klines(symbol, interval, start, **kwargs)
    df = pd.DataFrame(raw_data, columns=kline_columns).set_index('CloseTime')
    return pd.to_numeric(df.Close).rename(symbol)


def get_price_data(fiat, max_symbols=None, **kwargs):
    symbols = get_trading_symbols(fiat=fiat)
    max_symbols = max_symbols or len(symbols)
    return pd.concat([get_klines(symbol, **kwargs) for symbol in tqdm(symbols[:max_symbols], desc='Collecting data')], 1).dropna()


