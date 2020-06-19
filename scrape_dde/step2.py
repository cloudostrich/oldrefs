# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 09:55:42 2017

@author: User
"""
import pandas as pd

CACHE = {}
STORE = 'store.h5'   # Note: another option is to keep the actual file open

def process_row(d, key, max_len=5000, _cache=CACHE):
    """
	Creates a dict with key holding a list of dicts of tick data
    Append row d to the store 'key'.

    When the number of items in the key's cache reaches max_len,
    append the list of rows to the HDF5 store and clear the list.
    """
    # keep the rows for each key separate.
    lst = _cache.setdefault(key, []) #set default key for dict CACHE
    if len(lst) >= max_len:
        store_and_clear(lst, key)
    lst.append(d)

def store_and_clear(lst, key):
    """
    Convert key's cache list to a DataFrame and append that to HDF5.
    """
    df = pd.DataFrame(lst)
    with pd.HDFStore(STORE) as store:
        store.append(key, df)
    lst.clear()

def get_latest(key, _cache=CACHE):
    store_and_clear(_cache[key], key)
    with pd.HDFStore(STORE) as store:
        return store[key]


def test1():
    for k, lst in CACHE.items():  # you can instead use .iteritems() in python 2
        store_and_clear(lst, k)
		
'''    
process_row({'time' :'2013-01-01 00:00:00', 'stock' : 'BLAH', 'high' : 4.0, 'low' : 3.0, 'open' : 2.0, 'close' : 1.0}, key="df")

for k, lst in CACHE.items():  # you can instead use .iteritems() in python 2
    store_and_clear(lst, k)
    
with pd.HDFStore(STORE) as store:
    df = store["df"]                    # other keys will be store[key]
	
df = get_latest("df")
'''