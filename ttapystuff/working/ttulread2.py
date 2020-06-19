import clr
import sys

sys.path.append(r'C:\tt\ttapi\bin')
clr.AddReference('TradingTechnologies.TTAPI')
from System import Object
from System import Action
from System import Threading
from System import ValueType
from System import Enum
#from System import IDisposable
import TradingTechnologies.TTAPI as ttapi

#class TTAPIFunctions(IDisposable):
class TTAPIFunctions():
    """
    <summary>
    Main TT API class
    </summary>
    """
    def __init__(self, u ,p):
        self.m_apiInstance = None
        self.m_disp = None
        self.m_disposed = False
        #self.m_lock = Object()
        self.m_req = None
        self.m_ps = None
        self.m_username = u
        self.m_password = p

    def Start(self):
        """
        <summary>
        Create and start the Dispatcher
        </summary>
        """
        # Attach a WorkerDispatcher to the current thread
        self.m_disp = ttapi.Dispatcher.AttachWorkerDispatcher()
        self.m_disp.BeginInvoke(Action(self.Init))
        self.m_disp.Run()

    def Init(self):
        """
        <summary>
        Initialize TT API
        </summary>
        """
        # Use "XTraderMode Login" Login Mode
        h = ttapi.ApiInitializeHandler(self.ttApiInitComplete)
        ttapi.TTAPI.CreateUniversalLoginTTAPI(ttapi.Dispatcher.Current, self.m_username, self.m_password, h)

    def ttApiInitComplete(self, api, ex):
        """ <summary>
        Event notification for status of TT API initialization
        </summary>
        """
        if ex == None:
            # Authenticate your credentials
            self.m_apiInstance = api
            self.m_apiInstance.AuthenticationStatusUpdate += self.m_apiInstance_AuthenticationStatusUpdate
            self.m_apiInstance.Start()
        else:
            print("TT API Initialization Failed: {0}".format(ex.Message))
            self.Dispose()

    def m_apiInstance_AuthenticationStatusUpdate(self, sender, e):
        """
        <summary>
		 Event notification for status of authentication
		 </summary>
        """
        if e.Status.IsSuccess:
            # Add code here to begin working with the TT API
            # lookup an instrument
            self.m_req = ttapi.InstrumentLookupSubscription(self.m_apiInstance.Session, 
			ttapi.Dispatcher.Current, ttapi.ProductKey(ttapi.MarketKey.Cme, ttapi.ProductType.Future, "YM"), "Jun17")
            self.m_req.Update += self.m_req_Update
            print("Connection Success!")
            self.m_req.Start()
        else:
            print("TT Login failed: {0}".format(e.Status.StatusMessage))
            self.Dispose()

    def m_req_Update(self, sender, e):
        """
        <summary>
		 Event notification for instrument lookup
		 </summary>
        """
        if e.Instrument != None and e.Error == None:
            # Instrument was found
            print("Found: {0}".format(e.Instrument.Name))
            # Subscribe for Inside Market Data
            self.m_ps = ttapi.PriceSubscription(e.Instrument, ttapi.Dispatcher.Current)
            self.m_ps.Settings = ttapi.PriceSubscriptionSettings(ttapi.PriceSubscriptionType.InsideMarket)
            self.m_ps.FieldsUpdated += self.m_ps_FieldsUpdated
            self.m_ps.Start()
        elif e.IsFinal:
            # Instrument was not found and TT API has given up looking for it
            print("Cannot find instrument: {0}".format(e.Error.Message))
            self.Dispose()

    def m_ps_FieldsUpdated(self, sender, e):
        """
        <summary>
		 Event notification for price update
		 </summary>
        """
        ltp = e.Fields.GetLastTradedPriceField()
        ltq = e.Fields.GetLastTradedQuantityField()
        print("ltp and ltq success...")
        if ltp.HasChanged or ltq.HasChanged:
            print(ltp.Value, ltq.Value)
        print('haschanged seems ok')
##        if e.Error == None:
##            if e.UpdateType == ttapi.UpdateType.Snapshot:
##                # Received a market data snapshot
##                print("Market Data Snapshot:")
##                thingy = e.Fields.GetFieldIds().GetEnumerator()
##                while thingy.MoveNext():
##                    id = thingy.Current
##                    print("    {0} : {1}".format(id, e.Fields[id].FormattedValue)) #id.ToString()
##            else:
##                # Only some fields have changed
##                print("Market Data Update:")
##                thingy = e.Fields.GetChangedFieldIds().GetEnumerator()
##                while thingy.MoveNext():
##                    id = thingy.Current
##                    print("    {0} : {1}".format(id, e.Fields[id].FormattedValue))
##        else:
##            if e.Error.IsRecoverableError == False:
##                print("Unrecoverable price subscription error: {0}".format(e.Error.Message))
##                self.Dispose()

    def Dispose(self):
        """
        <summary>
        Shuts down the TT API
        </summary>
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
        #Begin shutdown the TT API
        ttapi.TTAPI.ShutdownCompleted += self.TTAPI_ShutdownCompleted
        ttapi.TTAPI.Shutdown()
        self.m_disposed = True

	# Unattached callbacks and dispose of all subscriptions
	# Begin shutdown the TT API
    def TTAPI_ShutdownCompleted(self, sender, e):
        """ <summary>
		 Event notification for completion of TT API shutdown
		 </summary>
        """
        # Shutdown the Dispatcher
        if self.m_disp != None:
            self.m_disp.BeginInvokeShutdown()
            self.m_disp = None

            
tf = TTAPIFunctions("CHOODTS","12345678")
if __name__ == '__main__':
    tf.Start()
