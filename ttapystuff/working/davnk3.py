import pandas as pd

SCACHE = {}
SSTORE = 'strategy1.h5'
MINR = 35
LIVESIM = False

store = pd.HDFStore('strategy1.h5')
##DFraw = store['raw'].tail()
##DF5 = store['bar5'].ix[-MINR:]
##DF15 = store['bar15'].ix[-MINR:]
##DF60 = store['bar60'].ix[-MINR:]
NETPOS=0
ENTRY = None
TICKSIZE = 5

##h3 = pd.read_hdf('nktest1.h5')
##o3 = h3['close'].resample('5Min').ohlc()
##o3= o3[o3['low']>0]
##o3.index[0]
##m5 = pd.Timedelta('0days 00:05:00')

def EMA(data_frame, spn, minp):
    return pd.ewma(data_frame['close'], span=spn, min_periods = minp)

def MACD(ohlc, f=12, s=26, m=9):
    fast_ema = pd.ewma( ohlc.close, span=f, min_periods = f)
    slow_ema = pd.ewma( ohlc.close, span=s, min_periods = s)
    macd = fast_ema - slow_ema
    macd_sig = pd.ewma( macd, span = m)
    hist = macd - macd_sig
    return pd.DataFrame( {"MACD_hist":hist, "MACD_sig":macd_sig,
                        "MACD":macd}, index=[ohlc.index])

def macd1(df, f=12, s=26):
    fast_ema = pd.ewma( ohlc.close, span=f, min_periods = f)
    slow_ema = pd.ewma( ohlc.close, span=s, min_periods = s)
    macd = fast_ema - slow_ema
    return macd

def macdSig(macd, m=9):
    return pd.ewma( macd, span = m, min_periods=m)

def macdHist(macd, macd_signal):
    return macd - macd_signal

    
def ohlcGet(raw_dat, colname, tf):
    df = raw_dat[colname].resample(tf).ohlc()
    df = df[df[colname]>0]
    return df
    
def store_and_clear(self, lst, key):
    """
    Convert key's cache list to a DataFrame and append that to HDF5.
    """
    df = pd.DataFrame(lst)
    df.set_index(['time'], inplace = True)
    with pd.HDFStore(SSTORE) as store:
        store.append(key, df)
    lst.clear()

def get_latest(self, key):
    store_and_clear(SCACHE[key], key)
    with pd.HDFStore(SSTORE) as store:
        return store[key]
    
def check12long(df):
    if (df.ix[-1]['close'] > df.ix[-1]['open']) and (df.ix[-1]['close']>df.ix[-2]['close']):
        if (df.ix[-1]['close'] > df.ix[-1]['ema10']) and (df.ix[-1]['close']>df.ix[-1]['ema20']):
            if (df.ix[-1]['ema10'] - df.ix[-2]['ema10'])>2:
                if (df.ix[-1]['macd'] > df.ix[-1]['macdsig']) and (df.ix[-1]['macdhist']>df.ix[-2]['macdhist']):
                    return True
    else:
        return False

def check5long(df):
    if (df.ix[-1]['close'] > df.ix[-1]['high']):
        if (df.ix[-1]['close'] > df.ix[-1]['ema10']) and (df.ix[-1]['ema10']>df.ix[-1]['ema20']):
            if (df.ix[-1]['macd'] > df.ix[-1]['macdsig']) and (df.ix[-1]['macdhist']>df.ix[-2]['macdhist']):
                if NETPOS=0:
                    return True
    else:
        return False
    
def checkExlong(d5, d15):
    if NETPOS > 0:
        if ((d5.ix[-1]['close'] < (ENTRY-2*TICKSIZE) ) or (d5.ix[-1]['close']<(df.ix[-2]['low']-1*TICKSIZE)) or
            (d5.ix[-1]['close']<(df.ix[-3]['low']-1*TICKSIZE)) or (df.ix[-1]['close']>df.ix[-4]['low'])):
            return True
        elif (((d15.ix[-1]['high'] - d15.ix[-1]['close'])>3*TICKSIZE) or (((d15.ix[-2]['high']-df.ix[-1]['close'])>3*TICKSIZE) and
            (d5.ix[-1]['open']>df.ix[-1]['close']))):
            return True
        else:
            return False    
    return False

def check12short(df):
    if (df.ix[-1]['close'] < df.ix[-1]['open']) and (df.ix[-1]['close']<df.ix[-2]['close']):
        if (df.ix[-1]['close'] < df.ix[-1]['ema10']) and (df.ix[-1]['close']<df.ix[-1]['ema20']):
            if (df.ix[-2]['ema10'] - df.ix[-1]['ema10'])>2:
                if (df.ix[-1]['macd'] < df.ix[-1]['macdsig']) and (df.ix[-1]['macdhist']<df.ix[-2]['macdhist']):
                    return True
    else:
        return False

def check5short(df):
    if (df.ix[-1]['close'] < df.ix[-1]['low']):
        if (df.ix[-1]['close'] < df.ix[-1]['ema10']) and (df.ix[-1]['ema10']<df.ix[-1]['ema20']):
            if (df.ix[-1]['macd'] < df.ix[-1]['macdsig']) and (df.ix[-1]['macdhist']<df.ix[-2]['macdhist']):
                if NETPOS=0:
                    return True
    else:
        return False
    
def checkExshort(d5, d15):
    if NETPOS < 0:
        if ((d5.ix[-1]['close'] > (ENTRY+2*TICKSIZE) ) or (d5.ix[-1]['close']>(df.ix[-2]['high']+1*TICKSIZE)) or
            (d5.ix[-1]['close']>(df.ix[-3]['high']+1*TICKSIZE)) or (df.ix[-1]['close']>df.ix[-4]['high'])):
            return True
        elif (((d15.ix[-1]['close'] - d15.ix[-1]['low'])>3*TICKSIZE) or (((d15.ix[-2]['close']-df.ix[-1]['low'])>3*TICKSIZE) and
            (d5.ix[-1]['close']>df.ix[-1]['open']))):
            return True
        else:
            return False    
    return False
            
def dfRam(dfr, dfk, tf):
    global dfk
    dfrcln = dfr[dfr.index>dfk.index[-1]]
    oh = ohlcGet(dfrcln, 'raw', tf)
    if len(oh)>1:
        dfk = dfk.append(oh.ix[:-1])
        dfk = dfk.ix[-40:]
        oh = oh.ix[-1]
    ts = dfk.append(oh)
    ts['ema10'] = pd.ewma(ts['close'], span = 10, min_periods = 10)
    ts['ema20'] = pd.ewma(ts['close'], span = 20, min_periods = 20)
    ts['macd'] = macd1(ts['close'])
    ts['macdsig'] = macdSig(ts['macd'])
    ts['macdhist'] = macdHist(ts['macd'], ts['macd_signal'])
    ts = ts.tail()
    return ts

def buyMartket():
    """ buy market either in live or sim mode
    """


def sellMarket():
    """ buy market either in live or sim mode
    """
    

    
def newraw(d, max_len=500):
    """
        Creates a dict with key holding a list of dicts of tick data
        Append row d to the store 'key'.

        When the number of items in the key's cache reaches max_len,
        append the list of rows to the HDF5 store and clear the list.
    """
    livelst = SCACHE.setdefault('raw',[])
    if len(lst) >= max_len:
        self.store_and_clear(lst, 'raw')
    lst.append(d)
    DFraw = pd.DataFrame(lst)
    DFraw.set_index(['time'], inplace = True)
    d60 = dfRam(DFraw, DF60, '60Min')
    d15 = dfRam(DFraw, DF15, '15Min')
    d5 = dfRam(DFraw, DF5, '5Min')

    
    if NETPOS = 0:
        if check12long(d60):
            if check12long(d15):
                if check5short(d5):
                    buyMarket()
        elif check12short(d60):
            if check12short(d15):
                if check5short(d5):
                    sellMarket()
    elif NETPOS > 0:
        if checkExlong(d5, d15):
            sellMarket()
    elif NETPOS < 0:
        if checkExshort(d5, d15):
            buyMarket()
    else:
        pass

def saveNclose():
    """save all dfs to hdf b4 main dispose
    """
    
