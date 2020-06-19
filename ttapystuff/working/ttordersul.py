    import clr
import sys

sys.path.append(r'C:\tt\ttapi\bin')
clr.AddReference('TradingTechnologies.TTAPI')

from System import Object
from System import Action
#from System import Threading
#from System import IDisposable
#from System import ValueType
#from System import Enum
#from System.Collections.Generic import *
#from System.Linq import *
#from System.Text import *
import TradingTechnologies.TTAPI as ttapi
import TradingTechnologies.TTAPI.Tradebook as tradebk

#class TTAPIFunctions(IDisposable):
class TTAPIFunctions():
    """ <summary>
     Main TT API class
     </summary>
    """
    # <summary>
    # Declare the TTAPI objects
    # </summary>
    def __init__(self, u, p):
        """ <summary>
         Private default constructor
         </summary>
        """
        self.m_apiInstance = None
        self.m_disp = None
        self.m_disposed = False
        self.m_lock = Object()
        self.m_req = None
        self.m_ps = None
        self.m_ts = None
        self.m_orderKey = ""
        self.m_username = u
        self.m_password = p

    def Start(self):
        """ <summary>
         Create and start the Dispatcher
         </summary>
        """
        # Attach a WorkerDispatcher to the current thread
        self.m_disp = ttapi.Dispatcher.AttachWorkerDispatcher()
        self.m_disp.BeginInvoke(Action(self.Init))
        self.m_disp.Run()

    def Init(self):
        """ <summary>
         Initialize TT API
         </summary>
        """
        # Use "Universal Login" Login Mode
        h = ttapi.ApiInitializeHandler(self.ttApiInitComplete)
        ttapi.TTAPI.CreateUniversalLoginTTAPI(ttapi.Dispatcher.Current, self.m_username, self.m_password,h)

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
            self.m_req = ttapi.InstrumentLookupSubscription(self.m_apiInstance.Session, ttapi.Dispatcher.Current, ttapi.ProductKey(ttapi.MarketKey.Cme, ttapi.ProductType.Future, "YM"), "Jun17")
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
            # Create a TradeSubscription to listen for order / fill events only for orders submitted through it
            self.m_ts = tradebk.InstrumentTradeSubscription(self.m_apiInstance.Session, ttapi.Dispatcher.Current, e.Instrument, True, True, False, False)
            self.m_ts.OrderUpdated += self.m_ts_OrderUpdated
            self.m_ts.OrderAdded += self.m_ts_OrderAdded
            self.m_ts.OrderDeleted += self.m_ts_OrderDeleted
            self.m_ts.OrderFilled += self.m_ts_OrderFilled
            self.m_ts.OrderRejected += self.m_ts_OrderRejected
            self.m_ts.Start()
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
        if e.Error == None:
            # Make sure that there is a valid bid
            if e.Fields.GetBestBidPriceField().HasValidValue:
                if self.m_orderKey == "":
                    # If there is no order working, submit one through the first valid order feed.
                    # You should use the order feed that is valid for your purposes.
                    op = ttapi.OrderProfile(e.Fields.Instrument.GetValidOrderFeeds()[0], e.Fields.Instrument)
                    op.BuySell = ttapi.BuySell.Buy
                    op.AccountName = "12345678"
                    op.AccountType = ttapi.AccountType.A1
                    op.OrderQuantity = ttapi.Quantity.FromInt(e.Fields.Instrument, 1)
                    op.OrderType = ttapi.OrderType.Limit
                    op.LimitPrice = e.Fields.GetBestBidPriceField().Value
                    if not self.m_ts.SendOrder(op):
                        print("Send new order failed.  {0}".format(op.RoutingStatus.Message))
                        self.Dispose()
                    else:
                        self.m_orderKey = op.SiteOrderKey
                        print("Send new order succeeded.")
                elif self.m_ts.Orders.ContainsKey(self.m_orderKey) and self.m_ts.Orders[self.m_orderKey].LimitPrice != e.Fields.GetBestBidPriceField().Value:
                    # If there is a working order, reprice it if its price is not the same as the bid
                    op = self.m_ts.Orders[self.m_orderKey].GetOrderProfile()
                    op.LimitPrice = e.Fields.GetBestBidPriceField().Value
                    op.Action = ttapi.OrderAction.Change
                    if not self.m_ts.SendOrder(op):
                        print("Send change order failed.  {0}".format(op.RoutingStatus.Message))
                    else:
                        print("Send change order succeeded.")
        else:
            if e.Error.IsRecoverableError == False:
                print("Unrecoverable price subscription error: {0}".format(e.Error.Message))
                self.Dispose()

    def m_ts_OrderRejected(self, sender, e):
        """ 
         <summary>
         Event notification for order rejected
         </summary>
        """
        print("Order was rejected. {0}".format(e.Message))

    def m_ts_OrderFilled(self, sender, e):
        """ 
         <summary>
         Event notification for order filled
         </summary>
        """
        if e.FillType == ttapi.FillType.Full:
            print("Order was fully filled for {0} at {1}.".format(e.Fill.Quantity, e.Fill.MatchPrice))
        else:
            print("Order was partially filled for {0} at {1}.".format(e.Fill.Quantity, e.Fill.MatchPrice))
        print("Average Buy Price = {0} : Net Position = {1} : P&L = {2}".format(self.m_ts.ProfitLossStatistics.BuyAveragePrice, self.m_ts.ProfitLossStatistics.NetPosition, self.m_ts.ProfitLoss.AsPrimaryCurrency))

    def m_ts_OrderDeleted(self, sender, e):
        """ 
         <summary>
         Event notification for order deleted
         </summary>
        """
        print("Order was deleted.")

    def m_ts_OrderAdded(self, sender, e):
        """ 
         <summary>
         Event notification for order added
         </summary>
        """
        print("Order was added with price of {0}.".format(e.Order.LimitPrice))

    def m_ts_OrderUpdated(self, sender, e):
        """ 
         <summary>
         Event notification for order update
         </summary>
        """
        print("Order was updated with price of {0}.".format(e.NewOrder.LimitPrice))

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
        if self._m_disp != None:
            self._m_disp.BeginInvokeShutdown()
            self._m_disp = None

tf = TTAPIFunctions("CHOODTS","12345678")
