from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from TradingTechnologies.TTAPI import *

class TTAPIFunctions(IDisposable):
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
		self._m_apiInstance = None
		self._m_disp = None
		self._m_disposed = False
		self._m_lock = System.Object()
		self._m_req = None
		self._m_ps = None
		self._m_username = ""
		self._m_password = ""
		# <summary>
		# Primary constructor
		# </summary>
		self._m_username = u
		self._m_password = p

	def __init__(self, u, p):
		self._m_apiInstance = None
		self._m_disp = None
		self._m_disposed = False
		self._m_lock = System.Object()
		self._m_req = None
		self._m_ps = None
		self._m_username = ""
		self._m_password = ""
		self._m_username = u
		self._m_password = p

	def Start(self):
		""" <summary>
		 Create and start the Dispatcher
		 </summary>
		"""
		# Attach a WorkerDispatcher to the current thread
		self._m_disp = Dispatcher.AttachWorkerDispatcher()
		self._m_disp.BeginInvoke(Action(Init))
		self._m_disp.Run()

	def Init(self):
		""" <summary>
		 Initialize TT API
		 </summary>
		"""
		# Use "Universal Login" Login Mode
		h = ApiInitializeHandler(ttApiInitComplete)
		TTAPI.CreateUniversalLoginTTAPI(Dispatcher.Current, self._m_username, self._m_password, h)

	def ttApiInitComplete(self, api, ex):
		""" <summary>
		 Event notification for status of TT API initialization
		 </summary>
		"""
		if ex == None:
			# Authenticate your credentials
			self._m_apiInstance = api
			self._m_apiInstance.AuthenticationStatusUpdate += self.apiInstance_AuthenticationStatusUpdate
			self._m_apiInstance.Start()
		else:
			Console.WriteLine("TT API Initialization Failed: {0}", ex.Message)
			self.Dispose()

	def apiInstance_AuthenticationStatusUpdate(self, sender, e):
		""" <summary>
		 Event notification for status of authentication
		 </summary>
		"""
		if e.Status.IsSuccess:
			# Insert other code here that will run on this thread
			# lookup an instrument
			self._m_req = InstrumentLookupSubscription(self._m_apiInstance.Session, Dispatcher.Current, ProductKey(MarketKey.Cme, ProductType.Future, "ES"), "Dec13")
			self._m_req.Update += self.m_req_Update
			self._m_req.Start()
		else:
			Console.WriteLine("TT Login failed: {0}", e.Status.StatusMessage)
			self.Dispose()

	def m_req_Update(self, sender, e):
		""" <summary>
		 Event notification for instrument lookup
		 </summary>
		"""
		if e.Instrument != None and e.Error == None:
			# Instrument was found
			Console.WriteLine("Found: {0}", e.Instrument.Name)
			# Subscribe for Inside Market Data
			self._m_ps = PriceSubscription(e.Instrument, Dispatcher.Current)
			self._m_ps.Settings = PriceSubscriptionSettings(PriceSubscriptionType.InsideMarket)
			self._m_ps.FieldsUpdated += self.m_ps_FieldsUpdated
			self._m_ps.Start()
		elif e.IsFinal:
			# Instrument was not found and TT API has given up looking for it
			Console.WriteLine("Cannot find instrument: {0}", e.Error.Message)
			self.Dispose()

	def m_ps_FieldsUpdated(self, sender, e):
		""" <summary>
		 Event notification for price update
		 </summary>
		"""
		if e.Error == None:
			if e.UpdateType == UpdateType.Snapshot:
				# Received a market data snapshot
				Console.WriteLine("Market Data Snapshot:")
				enumerator = e.Fields.GetFieldIds().GetEnumerator()
				while enumerator.MoveNext():
					id = enumerator.Current
					Console.WriteLine("    {0} : {1}", id.ToString(), e.Fields[id].FormattedValue)
			else:
				# Only some fields have changed
				Console.WriteLine("Market Data Update:")
				enumerator = e.Fields.GetChangedFieldIds().GetEnumerator()
				while enumerator.MoveNext():
					id = enumerator.Current
					Console.WriteLine("    {0} : {1}", id.ToString(), e.Fields[id].FormattedValue)
		else:
			if e.Error.IsRecoverableError == False:
				Console.WriteLine("Unrecoverable price subscription error: {0}", e.Error.Message)
				self.Dispose()

	def Dispose(self):
		""" <summary>
		 Shuts down the TT API
		 </summary>
		"""

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
