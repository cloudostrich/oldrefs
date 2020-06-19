import clr
import sys
import pandas as pd

sys.path.append(r'C:\tt\ttapi\bin')
clr.AddReference('TradingTechnologies.TTAPI')
import TradingTechnologies.TTAPI as ttapi
from System import Object, Threading, ValueType, Enum
from System import Action

class TTAPIReader():
    """
    Main TT API class
    """
    def __init__(self):
        self.m_apiInstance = None
        self.m_disp = None
        self.m_disposed = False
        self.m_req = None
        self.m_ps = None
        # contract details
        self.instrMonth = "Dec17"
        self.instr = "ES"
        self.instrexch = ttapi.MarketKey.Cme
        self.instrType = ttapi.ProductType.Future

    def Start(self):
        """
Create  and start the Dispatcher
"""
        # Attach a WorkerDispatcher to the current thread
        self.m_disp = ttapi.Dispatcher.AttachWorkerDispatcher()
        self.m_disp.BeginInvoke(Action(self.Init))
        self.m_disp.Run()

    def Init(self):
        """
Initialize TT API
"""
        # Use XtraderMode Login
        h = ttapi.ApiInitializeHandler(self.ttApiInitComplete)
        ttapi.TTAPI.CreateXTraderModeTTAPI(ttapi.Dispatcher.Current, h)

    def ttApiInitComplete(self, api, ex):
        """
Event Notification for status of TT API Initialization
"""
        if ex == None:
            # Authenticate credentials
            self.m_apiInstance = api
            self.m_apiInstance.ConnectionStatusUpdate += self.m_apiInstance_ConnectionStatusUpdate
            self.m_apiInstance.Start()
        else:
            print("TT API Initialization Failed: {0}".format(ex.Message))
            self.Disposed()

    def m_apiInstance_ConnectionStatusUpdate(self, sender, e):
        """
Event notification for status of authentication
"""
        if e.Status.IsSuccess:
            # Add code here to begin working with the TT API
            # lookup an instrument
            print("Connection Success!")
            self.m_req = ttapi.InstrumentLookupSubscription(self.m_apiInstance.Session,
                                                            ttapi.Dispatcher.Current,
                                                            ttapi.ProductKey(self.instrexch, self.instrType, self.instr),
                                                            self.instrMonth)
            self.m_req.Update += self.m_req_Update
            self.m_req.Start()
        else:
            print("TT login failed: {0}".format(e.Status.StatusMessage))
            self.Dispose()

    def m_req_Update(self, sender, e):
        """
Event notification for instrument lookup
"""
        if e.Instrument !=None and e.Error == None:
            # Means Instrument was found
            print("Found: {0}".format(e.Instrument.Name))
            # Subscribe for Inside Market Data
            self.m_ps = ttapi.PriceSubscription(e.Instrument, ttapi.Dispatcher.Current)
            self.m_ps.Settings = ttapi.PriceSubscriptionSettings(ttapi.PriceSubscriptionType.InsideMarket)
            self.m_ps.Start()
        elif e.IsFinal:
            # Instrument was not found and TT API has given up looking for it
            print("Cannot find instrument: {0}".format(e.Error.Message))
            self.Dispose()

    def m_ps_FieldsUpdated(self, sender,e):
        """
Event notification for price update
"""
        ltp = e.Fields.GetLastTradedPriceField()
        ltq = e.Fields.GetLastTradedQuantityField()
        print("ltp and ltq success...")
        if ltp.HasChanged or ltq.HasChanged:
            print(ltp.Value, ltq.Value)
            # send to process row here

    def Dispose(self):
        """
Shuts down the TT API
"""
        if not self.m_disposed:
            if (self.m_req != None):
                self.m_req.Update -= self.m_req_Update
                self.m_req.Dispose()
                self.m_req = None
            if (self.m_ps != None):
                self.m_ps.FieldsUpdated -= self.m_ps_FieldsUpdated
                self.m_ps.Dispose()
                self.m_ps = None

        # Begin shutdown the TT API
        ttapi.TTAPI.ShutdownCompleted += self.TTAPI_ShutdownCompleted
        ttapi.TTAPI.Shutdown()
        self.m_disposed = True

    def TTAPI_ShutdownCompleted(self, sender , e):
        """
Event notification for completion of TT API shutdown
"""
        # Shutdown the Dispatcher
        if self.m_disp != None:
            self.m_disp.BeginInvokeShutdown()
            self.m_disp = None


"""
tr = TTAPIReader()
tr.Start()
"""
