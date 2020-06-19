from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file

import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

h3 = pd.read_hdf('hdtest3.h5')
o3 = h3['close'].resample('15Min').ohlc()

def readFile(filename):
  return pd.read_hdf(filename)

def convertOhlc(raw_dat, tf):
  return raw_dat['close'].resample(tf).ohlc()

def MACD(ohlc, f=12, s=26, m=9):
  fast_ema = pd.ewma( ohlc.close, span=f)
  slow_ema = pd.ewma( ohlc.close, span=s)
  macd = fast_ema - slow_ema
  macd_sig = pd.ewma( macd, span=9)
  hist = macd - macd_sig
  return pd.DataFrame( {"MACD_hist":hist, "MACD":macd_sig}, index=[ohlc.index])

##def ewma(price, fast, slow):
##   fast_ewma = pd.ewma(price, span=fast)
##   slow_ewma = pd.ewma(price, span=slow)
##   raw_ewmac = fast_ewma - slow_ewma
##   vol = robust_vol_calc(price.diff())
##   return raw_ewmac /  vol

def rolling_ewma(data_frame, spn, minp):
    """
    rolling_ewma - Calculates exponentially weighted moving average
 
    Parameters
    ----------
    data_frame : DataFrame
        contains time series
    periods : int
        periods in the EWMA
 
    Returns
    -------
    DataFrame
    """
    # span = 2 / (1 + periods)
    return pd.ewma(data_frame, span=spn, min_periods = minp)

"""
plot in mpl
"""
def plot_candlestick(df, ax=None, fmt="%Y-%m-%d"):
    if ax is None:
        fig, ax = plt.subplots()
    idx_name = df.index.name
    dat = df.reset_index()[[idx_name,"time", 'open', 'high', 'low', 'close']]
    dat[df.index.name] = dat[df.index.name].apply(mdates.date2num)
    ax.xaxis_date()
##    ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    plt.xticks(rotation=45)
    _ = candlestick_ohlc(ax, dat.values, width=.6, colorup='g',colordown='r', alpha =1)
    ax.set_xlabel(idx_name)
    ax.set_ylabel("OHLC")
    return ax


ax = plot_candlestick(o3)
plt.tight_layout()
plt.show()
