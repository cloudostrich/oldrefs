# -*- coding: utf-8 -*-
# DDE code
import datetime
import pymongo
import win32ui
import dde
import time
import logging
from pymongo import MongoClient


LOG_FILE_PATH = "ddeerror.log"
LOGGER = None
MONGO_CLIENT = None
MONGO_URI = "mongodb://zhadmin:zhadmin99@128.199.128.182/admin"
INTERVAL = 1
SERVER = 'Excel'
TOPIC = "test3c.xls"
REQRANGE = "R2C1:R74C9"
CACHE = {}
CS = {
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 7,
    9: 8,
    0: 9,
    11: 10,
    14: 1,
    15: 2,
    16: 3,
    17: 4,
    18: 5,
    19: 6,
    22: 1,
    23: 2,
    24: 3,
    25: 4,
    26: 5,
    27: 6,
    28: 7,
    29: 8,
    30: 9,
    31: 10,
    32: 11,
    33: 12,
    36: 1,
    37: 2,
    38: 3,
    39: 4,
    40: 5,
    41: 6,
    42: 7,
    43: 8,
    44: 9,
    45: 10,
    46: 11,
    47: 12,
    49: 0,
    50: 0,
    62: 0,
    64: 0,
    65: 0,
    66: 0,
    68: 0,
    70: 0,
    72: 0
}

def dde_connect(svrnam,SERVER,TOPIC):
    #Create and connect to dde server
    svr=dde.CreateServer()
    svr.Create(svrnam)
    con=dde.CreateConversation(svr)
    con.ConnectTo(SERVER,TOPIC)
    return con

def dde_hit(c):
    now = datetime.datetime.now()
    feed = c.Request(REQRANGE).replace('\r\n','\n')
    feedtup = feed.split('\n')
    for k, c in CS.iteritems():
        line = feedtup[k]
        items = line.split('\t')
        tradetime = items[1]
        if len(tradetime) == 7:
            tradetime = "0" + tradetime
        record = {
            "shortname": items[0],
            "tradetime": tradetime,
            "last": items[2],
            "tvol": items[3],
            "buyq": items[4],
            "buy": items[5],
            "sell": items[6],
            "sellq": items[7],
            "openInt": items[8],
            "C": c
        }

        checksum = hash(frozenset(record.items()))
        if k not in CACHE or CACHE[k] != checksum:
            record["datetime"] = now
            CACHE[k] = checksum
            mongo_save(record)

def mongo_save(record):
    MONGO_CLIENT.admin.stocks.insert(record)

def init_logger():
    global LOGGER
    LOGGER = logging.getLogger('dde')
    hdlr = logging.FileHandler(LOG_FILE_PATH)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    LOGGER.addHandler(hdlr)
    LOGGER.setLevel(logging.WARNING)

if __name__ == '__main__':
    init_logger()
    con = dde_connect('test4',SERVER,TOPIC)
    while True:
        try:
            
            MONGO_CLIENT = pymongo.MongoClient(MONGO_URI)
            while True:
                dde_hit(con)
                #time.sleep(INTERVAL)
        except Exception as e:
            LOGGER.error(str(e))
            print str(e)
            time.sleep(10)
