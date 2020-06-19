import urllib2
import json
import re
import datetime
import sqlite3

conn = sqlite3.connect('dev.db')
now = datetime.datetime.today()
    
def create(contract, month_year, last = None, from_prev = None, bid = None, ask = None, open = None, high = None, low = None, close = None, vol = None, open_int = None, settle = None, prev_settle = None):
  with conn:
    cur = conn.cursor()    
    cur.execute("""INSERT INTO future_info
                    (contract, month_year, recorded_at, 
                    last, from_prev, bid, ask, 
                    open, high, low, close, 
                    vol, open_int, settle, prev_settle)
                    VALUES 
                    (?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?)""", 
                 (contract, month_year, now,
                 last, from_prev, bid, ask,
                 open, high, low, close,
                 vol, open_int, settle, prev_settle))

#Sgx gives 2012 July as 2012-7 and 2012 December as 2012-12, this function standardize it as YYYYMM
def json_raw_my_to_month_year(my):
  year, _, month = my.partition('-')
  if int(month) < 10 :
    month = "0" + month
  return year + month

# For cleaning up the dojo-json, specific to sgx only because of special value like LUT
def tidy_dojo_futures(raw):
  raw = raw[5:].replace("{", "{\"").replace(",{", "^][^").replace("'", "\"").replace(":", "\":").replace(",", ",\"").replace("^][^", ",{")
  raw = re.sub(",\" label\"[^,]*,", ",", raw)
  raw = re.sub(".\"LUT\":[^\}]*\}", "}", raw)
  return raw

def main():
  url = "http://www.sgx.com/JsonRead/JsonData?qryId=NTP.Futures"
  raw = tidy_dojo_futures(urllib2.urlopen(url).read())
  json_raw = json.loads(raw)

  for item in json_raw['items']:
    create(item['CC'], json_raw_my_to_month_year(item['MY']), high=item["TH"])
    
main()
