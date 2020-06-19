from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file

h3 = pd.read_hdf('hdtest4.h5')
o3 = h3['close'].resample('60Min').ohlc()
o3= o3[o3['close']>0]

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
  return pd.DataFrame( {"MACD_hist":hist, "MACD_sig":macd_sig, "MACD":macd}, index=[ohlc.index])

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
    return pd.ewma(data_frame['close'], span=spn, min_periods = minp)

"""
plot in bokeh
"""
##o3['ema10'] = rolling_ewma(o3,10,10)

def candle(df):
    df.index.name='date'
    df = df.reset_index()
    df.date = df.date.apply(lambda x: str(x)[:10].replace(':','-') + str(x)[10:])
    df["date"] = pd.to_datetime(df["date"])

    inc = df.close > df.open
    dec = df.open > df.close
    w = 12*60*60*1000/70 # half day in ms

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = "my Candlestick")
    p.xaxis.major_label_orientation = 1


    p.segment(df.date, df.high, df.date, df.low, color="black")
    p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")
    p.line(df.date, df.ema10, line_width=2)

    ##output_file("candlestick.html", title="candlestick.py example")
    show(p)  # open a browser
