import clr
import sys
import pandas as pd

clr.AddReference('System.Windows')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
sys.path.append(r'C:\tt\ttapi\bin')
clr.AddReference('TradingTechnologies.TTAPI')

from System.Windows.Forms import Application, Form, Button, Label, Panel, StatusBar
from System.Drawing import Point, Color
from System import Object, Action, Threading, ValueType, Enum
#from System import IDisposable
import TradingTechnologies.TTAPI as ttapi


#class TTAPIFunctions(IDisposable):
class TTAPIReadForm(Form):
    """
    <summary>
    Main TT API class
    </summary>
    """
    def __init__(self):
        self.m_apiInstance = None
        self.m_disp = None
        self.m_handler = None
        self.m_disposed = False
        #self.m_lock = Object()
        self.m_req = None
        self.m_ps = None
        self.Text = 'DavTrader'
        self.Name = 'DavTrader'
        self.STORE = 'nktest2.h5'   # Note: another option is to keep the actual file open
        self.storekey = 'nk'
        self.CACHE = {}

        self.instrMonth = "Dec17"
        self.instr = "ES"
        self.instrexch = ttapi.MarketKey.Cme
        self.instrType = ttapi.ProductType.Future

        self.loginBtn = Button()
        self.loginBtn.Name = 'connect'
        self.loginBtn.Text = 'Connect'
        self.loginBtn.Location = Point(10, 10)
        self.loginBtn.Click += self.loginBtn_eventhandler

        self.DisposeBtn = Button()
        self.DisposeBtn.Name = 'disconnect'
        self.DisposeBtn.Text = 'Disconnect'
        self.DisposeBtn.Location = Point(100, 10)
        self.DisposeBtn.Click += self.DisposeBtn_eventhandler

        self.statusbar = StatusBar()
        self.statusbar.Parent = self

        self.Controls.Add(self.loginBtn)
        self.Controls.Add(self.DisposeBtn)

    def loginBtn_eventhandler(self, sender, event):
        ##tf = TTAPIFunctions("CHOODTS","12345678")
        name = sender.Name
        self.m_disp = ttapi.Dispatcher.AttachUIDispatcher()
        self.m_handler = ttapi.ApiInitializeHandler(tr.ttApiInitHandler)
        ttapi.TTAPI.CreateXTraderModeTTAPI(self.m_disp, self.m_handler)

    def DisposeBtn_eventhandler(self, sender, event):
        ##tf = TTAPIFunctions("CHOODTS","12345678")
        name = sender.Name
        self.Dispose()

    def process_row(self, d, key, max_len=1000):
        """
        Creates a dict with key holding a list of dicts of tick data
        Append row d to the store 'key'.

        When the number of items in the key's cache reaches max_len,
        append the list of rows to the HDF5 store and clear the list.
        """
        # keep the rows for each key separate.
        lst = self.CACHE.setdefault(key, []) #set default key for dict CACHE
        if len(lst) >= max_len:
            self.store_and_clear(lst, key)
        lst.append(d)
##        ohlc5 = ohlcConvert(lst, '5Min')
##        ohlc15 = ohlcConvert(lst, '15Min')
##        ohlc60 = ohlcConvert(lst, '60Min')
        

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
        self.store_and_clear(self.CACHE[key], key)
        with pd.HDFStore(self.STORE) as store:
            return store[key]

    def test1(self):
        for k, lst in self.CACHE.items():  # you can instead use .iteritems() in python 2
            store_and_clear(lst, k)

    def ttApiInitHandler(self, api, ex):
        """ <summary>
        Event notification for status of TT API initialization
        </summary>
        """
        if ex == None:
            # Authenticate your credentials
            self.m_apiInstance = api
            self.m_apiInstance.ConnectionStatusUpdate += self.m_apiInstance_ConnectionStatusUpdate
            self.m_apiInstance.Start()
            
            # below for submitting orders
            # m_customerDefaultsSubscription = new CustomerDefaultsSubscription(m_TTAPI.Session, Dispatcher.Current);
            # m_customerDefaultsSubscription.CustomerDefaultsChanged += new EventHandler(m_customerDefaultsSubscription_CustomerDefaultsChanged);
            # m_customerDefaultsSubscription.Start();
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
            self.m_req = ttapi.InstrumentLookupSubscription(self.m_apiInstance.Session, ttapi.Dispatcher.Current, ttapi.ProductKey(self.instrexch, self.instrType, self.instr), self.instrMonth)
            self.m_req.Update += self.m_req_Update
            self.statusbar.Text = 'Connection Success... YOU R IN!'
##            print("Connection Success!")
            self.m_req.Start()
        else:
            print("TT Login failed: {0}".format(e.Status.StatusMessage))
            self.statusbar.Text = "TT Login failed: {0}".format(e.Status.StatusMessage)
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
            self.statusbar.Text = "Found: {0}".format(e.Instrument.Name)
            # Subscribe for Inside Market Data
            self.m_ps = ttapi.PriceSubscription(e.Instrument, ttapi.Dispatcher.Current)
            self.m_ps.Settings = ttapi.PriceSubscriptionSettings(ttapi.PriceSubscriptionType.InsideMarket)
            self.m_ps.FieldsUpdated += self.m_ps_FieldsUpdated
            self.m_ps.Start()
        elif e.IsFinal:
            # Instrument was not found and TT API has given up looking for it
            print("Cannot find instrument: {0}".format(e.Error.Message))
            self.statusbar.Text = "Cannot find instrument: {0}".format(e.Error.Message)
            self.Dispose()
        else:
            print('Searching Instrument in progress...')
            self.statusbar.Text = 'Searching Instrument in progress...'

    def m_ps_FieldsUpdated(self, sender, e):
        """
        <summary>
		 Event notification for price update
		 </summary>
        """
        ltp = e.Fields.GetLastTradedPriceField()
        ltq = e.Fields.GetLastTradedQuantityField()
        if ltp.HasChanged:
            print(ltp.Value)
            ltp = ltp.Value
            ltpi = int(ltp.ToDouble())
            d = {'time' : pd.datetime.now(), 'raw' : ltpi}
            k = self.storekey
            self.process_row(d, k)
        
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
        self.statusbar.Text = 'Disconnected... U R OUT'

	# Unattached callbacks and dispose of all subscriptions
	# Begin shutdown the TT API
    def TTAPI_ShutdownCompleted(self, sender, e):
        """ <summary>
		 Event notification for completion of TT API shutdown
		 </summary>
        """
        # Shutdown the Dispatcher
        if self.m_disp != None:
            self.m_disp.Dispose()
            self.m_disp = None


tr = TTAPIReadForm()
Application.Run(tr)
