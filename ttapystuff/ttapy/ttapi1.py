# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 13:22:27 2017

@author: User
"""

import pythoncom
import time
import win32com.client as client
import win32com.client.gencache as gencache
import datetime as dt

GATE = None
NOTIFY = None

#class InstrNotify(getevents('XTAPI.TTInstrNotify')): 
# no need to use getevents as DispatchWithevents already does the getevents.
# So just defining your Events class without a base-class should work
class InstrNotify():
    def __init__(self):
        #self.close(self)
        pass

    def Subscribe(self, pInstr):
        self.AttachInstrument(pInstr)
        pInstr.Open(0)

    def OnNotifyFound(self, pNotify=None, pInstr=None):
        pInstr = client.Dispatch(pInstr)        
        print ("Found instrument:")
        print ('--> Contract: %s' % pInstr.Get('Contract'))
        print ('--> Exchange: %s' % pInstr.Get('Exchange'))

    def OnNotifyNotFound(self, pNotify=None, pInstr=None):
        pInstr = client.Dispatch(pInstr)        
        print ('Unable to find instrument')

    def OnNotifyUpdate(self, pNotify=None, pInstr=None):
        pInstr = client.Dispatch(pInstr)
        contract = pInstr.Get('Contract')

        bid = pInstr.Get('Bid')
        ask = pInstr.Get('Ask')
        last = pInstr.Get('Last')
        bidq = pInstr.Get('BidQty')
        askq = pInstr.Get('AskQty')
        lastq = pInstr.Get('LastQty')
        
        print ('[UPDATE] %s: %s--%s//%s--%s .. %s--%s   %s' % (contract, bidq, bid, ask, askq, last, lastq, str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        
        
def qq():
    GATE.XTAPITerminate()

    
def Connect():
    global NOTIFY, GATE
    #the below is required in order to establish the com-object links
    #that way you don't need to run makepy first
    gencache.EnsureModule('{A9595CA1-4980-11D5-ADF6-00508BAFB07F}', 0, 1, 0)

    GATE = gencache.EnsureDispatch('TradingTechnologies.TTAPI.TTAPI')
    NOTIFY = client.DispatchWithEvents('TTAPI.TTInstrNotify', InstrNotify)
    print('connected... ')

    
def getcme(pInstr):
    pInstr.Exchange = 'CME'
    pInstr.Product  = 'ES'
    pInstr.Contract = 'Mar17'
    pInstr.ProdType = 'FUTURE'
    print('cme es loaded')

    
def getstream(pin):
    NOTIFY.UpdateFilter = ('Last')
    NOTIFY.Subscribe(pin)
    print('..pumpin..')
    for i in range(10):
        pythoncom.PumpWaitingMessages()
        time.sleep(1.0)
        print('..sleeping..')

    
'''
def main():
    print('starting')
    Connect()
    
    pInstr = gencache.EnsureDispatch('XTAPI.TTInstrObj')
    #getcme(pInstr)
    pInstr.Exchange = 'CME'
    pInstr.Product  = 'ES'
    pInstr.Contract = 'Mar17'
    pInstr.ProdType = 'FUTURE'
    #getstream(pInstr)
    NOTIFY.UpdateFilter = ('Last')
    NOTIFY.Subscribe(pInstr)
    print('...waiting...')
    for i in range(10):
        pythoncom.PumpWaitingMessages()
        sleep(1.0)
        print('..sleepin..')

main()
'''