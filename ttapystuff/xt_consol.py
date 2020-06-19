// Conversion output is limited to 2048 chars
// Share Varycode on Facebook and tweet on Twitter
// to double the limits.

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
	def __init__(self):
		""" <summary>
		 Default constructor
		 </summary>
		"""
		self._m_apiInstance = None
		self._m_disp = None
		self._m_disposed = False
		self._m_lock = System.Object()

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
		# Use "Follow X_TRADER" Login Mode
		h = ApiInitializeHandler(ttApiInitComplete)
		TTAPI.CreateXTraderModeTTAPI(Dispatcher.Current, h)

	def ttApiInitComplete(self, api, ex):
		""" <summary>
		 Event notification for status of TT API initialization
		 </summary>
		"""
		if ex == None:
			# Authenticate your credentials
			self._m_apiInstance = api
			self._m_apiInstance.ConnectionStatusUpdate += self.m_apiInstance_ConnectionStatusUpdate
			self._m_apiInstance.Start()
		else:
			Console.WriteLine("TT API Initialization Failed: {0}", ex.Message)
			self.Dispose()

	def m_apiInstance_ConnectionStatusUpdate(self, sender, e):
		""" <summary>
		 Event notification for status of authentication
		 </summary>
		"""
		if e.Status.IsSuccess:
		else:
			# Add code here to begin working with the TT API
			Console.WriteLine("TT Login failed: {0}", e.Status.StatusMessage)
			self.Dispose()

	def Dispose(self):
		""" <summary>
		 Shuts down the TT API
		 </summary>
		"""

	# Begin shutdown the TT API
	def TTAPI_ShutdownCompleted(self, sender, e):
		""" <summary>
		 Event notification for completion of TT API shutdown
		 </summary>
		"""
		# S