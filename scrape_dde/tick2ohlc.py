import pandas as pd
 
data_frame = pd.read_csv('AUDJPY-2016-01.csv', names=['Symbol', 'Date_Time', 'Bid', 'Ask'],
 
 index_col=1, parse_dates=True)
 
data_frame.head()
 
data_ask =  data_frame['Ask'].resample('15Min').ohlc()
 
data_bid =  data_frame['Bid'].resample('15Min').ohlc()
 
data_ask.head()
 
data_bid.head()
 
data_ask_bid=pd.concat([data_ask, data_bid], axis=1, keys=['Ask', 'Bid'])