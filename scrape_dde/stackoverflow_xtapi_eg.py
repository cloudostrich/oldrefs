"""
http://stackoverflow.com/questions/14656579/how-to-connect-to-tt-x-trader-api-in-order-to-create-an-automated-trading-system

"""

import pythoncom
from time import sleep
from win32com.client import Dispatch, DispatchWithEvents, getevents
from win32com.client.gencache import EnsureDispatch, EnsureModule

GATE = None
NOTIFY = None

class InstrNotify(getevents('XTAPI.TTInstrNotify')):
    def __init__(self):
        pass

    def Subscribe(self, pInstr):
        self.AttachInstrument(pInstr)
        pInstr.Open(0)

    def OnNotifyFound(self, pNotify=None, pInstr=None):
        pInstr = Dispatch(pInstr)        
        print 'Found instrument:'
        print '--> Contract: %s' % pInstr.Get('Contract')
        print '--> Exchange: %s' % pInstr.Get('Exchange')

    def OnNotifyNotFound(self, pNotify=None, pInstr=None):
        pInstr = Dispatch(pInstr)        
        print 'Unable to find instrument'

    def OnNotifyUpdate(self, pNotify=None, pInstr=None):
        pInstr = Dispatch(pInstr)
        contract = pInstr.Get('Contract')

        bid = pInstr.Get('Bid')
        ask = pInstr.Get('Ask')
        last = pInstr.Get('Last')

        print '[UPDATE] %s: %s/%s' % (contract, bid, ask)


def Connect():
    global NOTIFY, GATE
    #the below is required in order to establish the com-object links
    #that way you don't need to run makepy first
    EnsureModule('{98B8AE14-466F-11D6-A27B-00B0D0F3CCA6}', 0, 1, 0)

    GATE = EnsureDispatch('XTAPI.TTGate')
    NOTIFY = DispatchWithEvents('XTAPI.TTInstrNotify', InstrNotify) 


def main():
    Connect()

    pInstr = EnsureDispatch('XTAPI.TTInstrObj')
    pInstr.Exchange = 'CME-A'
    pInstr.Product  = 'CL'
    pInstr.Contract = 'CL Mar13'
    pInstr.ProdType = 'FUTURE'

    NOTIFY.Subscribe(pInstr)

    for i in range(10):
        pythoncom.PumpWaitingMessages()
        sleep(1.0)

"""
If you have X_TRADER Pro up and running this will yield something like:

Found instrument:
--> Contract: CL Mar13
--> Exchange: CME-A
[UPDATE] CL Mar13: 9760/9764
"""
