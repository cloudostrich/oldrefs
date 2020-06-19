import clr
import sys
import pandas as pd

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
    def __init__(self):
        self.m_apiInstance = None
        self.m_disp = None
        self.m_disposed = False
        #self.m_lock = Object()
        self.m_req = None
        self.m_ps = None
        # contract details
        self.instrMonth = "Dec17"
        self.instr = "ES"
        self.instrexch = ttapi.MarketKey.Cme
        self.instrType = ttapi.ProductType.Future
        self.CACHE = {}
        self.STORE = 'storetest.h5'

    def process_row(self, d, key, max_len=50, _cache = 'c'):
        """
            Creates a dict with key holding a list of dicts of tick data
        Append row d to the store 'key'.

        When the number of items in the key's cache reaches max_len,
        append the list of rows to the HDF5 store and clear the list.
        """
        # keep the rows for each key separate.
##        lst = self.CACHE.setdefault(key, []) #set default key for dict CACHE
##        if len(lst) >= max_len:
##            store_and_clear(lst, key)
##        lst.append(d)
        print(d)
        print(key)
        print(max_len)

    def store_and_clear(self, lst, key):
        """
        Convert key's cache list to a DataFrame and append that to HDF5.
        """
        df = pd.DataFrame(lst)
        df.set_index(['time'], inplace = True)
        with pd.HDFStore(self.STORE) as store:
            store.append(key, df)
        lst.clear()

    def get_latest(self, key):
        store_and_clear(self.CACHE[key], key)
        with pd.HDFStore(STORE) as store:
            return store[key]


    def test1(self):
        for k, lst in self.CACHE.items():  # you can instead use .iteritems() in python 2
            store_and_clear(lst, k)

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
        ttapi.TTAPI.CreateXTraderModeTTAPI(ttapi.Dispatcher.Current, h)

    def ttApiInitComplete(self, api, ex):
        """ <summary>
        Event notification for status of TT API initialization
        </summary>
        """
        if ex == None:
            # Authenticate your credentials
            self.m_apiInstance = api
            self.m_apiInstance.ConnectionStatusUpdate += self.m_apiInstance_ConnectionStatusUpdate
            self.m_apiInstance.Start()
        else:
            print("TT API Initialization Failed: {0}".format(ex.Message))
            self.Dispose()

    def m_apiInstance_ConnectionStatusUpdate(self, sender, e):
        """
        <summary>
		 Event notification for status of authentication
		 </summary>
        """
        if e.Status.IsSuccess:
            # Add code here to begin working with the TT API
            # lookup an instrument
            self.m_req = ttapi.InstrumentLookupSubscription(self.m_apiInstance.Session,
                                                            ttapi.Dispatcher.Current,
                                                            ttapi.ProductKey(self.instrexch,
                                                                             self.instrType, self.instr),
                                                            self.instrMonth)
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
            #ltp = ltp.Value
            #ltpi = int(ltp.ToTicks())
            #self.process_row({'time' :pd.datetime.now(), 'close' : ltpi}, key = "nk")
        

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

            
#tf = TTAPIFunctions()
#if __name__ == '__main__':
 #   tf.Start()
