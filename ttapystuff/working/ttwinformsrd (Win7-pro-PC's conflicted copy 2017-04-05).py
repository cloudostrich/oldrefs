import clr
import sys

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
sys.path.append(r'C:\tt\ttapi\bin')
clr.AddReference('TradingTechnologies.TTAPI')

from System.Windows.Forms import Application, Form, Button, Label, Panel
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
        self.m_disposed = False
        #self.m_lock = Object()
        self.m_req = None
        self.m_ps = None

    # def Start(self):
        # """
        # <summary>
        # Create and start the Dispatcher
        # </summary>
        # """
        # # Attach a WorkerDispatcher to the current thread
        # self.m_disp = ttapi.Dispatcher.AttachUIDispathcer()
        # self.m_disp.BeginInvoke(Action(self.Init))
        # self.m_disp.Run()

    # def Init(self):
        # """
        # <summary>
        # Initialize TT API
        # </summary>
        # """
        # # Use "XTraderMode Login" Login Mode
        # h = ttapi.ApiInitializeHandler(self.ttApiInitComplete)
        # ttapi.TTAPI.CreateXTraderModeTTAPI(ttapi.Dispatcher.Current, h)

    # def ttApiInitComplete(self, api, ex):
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
            self.m_req = ttapi.InstrumentLookupSubscription(self.m_apiInstance.Session, ttapi.Dispatcher.Current, ttapi.ProductKey(ttapi.MarketKey.Sgx, ttapi.ProductType.Future, "NK"), "Jun17")
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
        else:
            print('Searching Instrument in progress...')

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

disp = ttapi.Dispatcher.AttachUIDispatcher()
tr = TTAPIReadForm()
m_handler = ttapi.ApiInitializeHandler(tr.ttApiInitHandler)
ttapi.TTAPI.CreateXTraderModeTTAPI(disp, m_handler)
Application.Run(tr)
