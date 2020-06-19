import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
clr.AddReference('System.Collections')
clr.AddReference('System.Collections.Generic')
clr.AddReference('System.ComponentModel')
clr.AddReference('TradingTechnologies.TTAPI')

from System import *
from System.Drawing import *
from System.Collections import *
from System.Collections.Generic import *
from System.ComponentModel import *
from System.Windows.Forms import *
from System.Data import *
from System.IO import *
from TradingTechnologies.TTAPI import *
from TradingTechnologies.TTAPI.Tradebook import *
from TradingTechnologies.TTAPI.WinFormsHelpers import *
from TradingTechnologies.TTAPI.CustomerDefaults import *

class frmSubmitOrder(Form):
	""" <summary>
	 SubmitOrder
	 
	 This example demonstrates using the TT API to submit an order.  The order types
	 available in the application are market, limit, stop market and stop limit.  
	 </summary>
	"""
	# Declare private TTAPI member variables.
	def __init__(self):
		self._m_TTAPI = None
		self._m_customerDefaultsSubscription = None
		self._m_instrumentTradeSubscription = None
		self._m_priceSubscription = None
		self._m_isShutdown = False
		self._m_shutdownInProcess = False
		self.InitializeComponent()

	def ttApiInitHandler(self, api, ex):
		""" <summary>
		 Init and start TT API.
		 </summary>
		 <param name="instance">XTraderModeTTAPI instance</param>
		 <param name="ex">Any exception generated from the ApiCreationException</param>
		"""
		if ex == None:
			self._m_TTAPI = api
			self._m_TTAPI.ConnectionStatusUpdate += self.ttapiInstance_ConnectionStatusUpdate
			self._m_TTAPI.Start()
            
			self._m_customerDefaultsSubscription = CustomerDefaultsSubscription(self._m_TTAPI.Session, Dispatcher.Current)
			self._m_customerDefaultsSubscription.CustomerDefaultsChanged += self.m_customerDefaultsSubscription_CustomerDefaultsChanged
			self._m_customerDefaultsSubscription.Start()
		elif not ex.IsRecoverable:
			MessageBox.Show("API Initialization Failed: " + ex.Message)

	def ttapiInstance_ConnectionStatusUpdate(self, sender, e):
		""" <summary>
		 ConnectionStatusUpdate callback.
		 Give feedback to the user that there was an issue starting up and connecting to XT.
		 </summary>
		"""
		if e.Status.IsSuccess:
			self._Enabled = True
		else:
			MessageBox.Show(String.Format("ConnectionStatusUpdate: {0}", e.Status.StatusMessage))

	def shutdownTTAPI(self):
		""" <summary>
		 Dispose of all the TT API objects and shutdown the TT API 
		 </summary>
		"""
		if not self._m_shutdownInProcess:
			# Dispose of all request objects
			if self._m_customerDefaultsSubscription != None:
				self._m_customerDefaultsSubscription.CustomerDefaultsChanged -= self.m_customerDefaultsSubscription_CustomerDefaultsChanged
				self._m_customerDefaultsSubscription.Dispose()
				self._m_customerDefaultsSubscription = None
			if self._m_instrumentTradeSubscription != None:
				self._m_instrumentTradeSubscription.OrderAdded -= self.m_instrumentTradeSubscription_OrderAdded
				self._m_instrumentTradeSubscription.OrderRejected -= self.m_instrumentTradeSubscription_OrderRejected
				self._m_instrumentTradeSubscription.Dispose()
				self._m_instrumentTradeSubscription = None
			if self._m_priceSubscription != None:
				self._m_priceSubscription.FieldsUpdated -= self.m_priceSubscription_FieldsUpdated
				self._m_priceSubscription.Dispose()
				self._m_priceSubscription = None
			TTAPI.ShutdownCompleted += self.TTAPI_ShutdownCompleted
			TTAPI.Shutdown()
		# only run shutdown once
		self._m_shutdownInProcess = True

	def TTAPI_ShutdownCompleted(self, sender, e):
		""" <summary>
		 Event fired when the TT API has been successfully shutdown
		 </summary>
		 <param name="sender"></param>
		 <param name="e"></param>
		"""
		self._m_isShutdown = True
		self.Close()

	def OnFormClosing(self, e):
		""" <summary>
		 Suspends the FormClosing event until the TT API has been shutdown
		 </summary>
		 <param name="e"></param>
		"""
		if not self._m_isShutdown:
			e.Cancel = True
			self.shutdownTTAPI()
		else:
			self.OnFormClosing(e)

	def Dispose(self, disposing):
		""" <summary>
		 Clean up any resources being used.
		 </summary>
		"""
		if disposing:
			if self._components != None:
				self._components.Dispose()
		self.Dispose(disposing)

	def InitializeComponent(self):
		""" <summary>
		 Required method for Designer support - do not modify
		 the contents of this method with the code editor.
		 </summary>
		"""
		self._components = System.ComponentModel.Container()
		self._sbaStatus = System.Windows.Forms.StatusBar()
		self._mainMenu1 = System.Windows.Forms.MainMenu(self._components)
		self._mnuAbout = System.Windows.Forms.MenuItem()
		self._gboInstrumentInfo = System.Windows.Forms.GroupBox()
		self._lblProductType = System.Windows.Forms.Label()
		self._txtProduct = System.Windows.Forms.TextBox()
		self._lblProduct = System.Windows.Forms.Label()
		self._lblExchange = System.Windows.Forms.Label()
		self._txtContract = System.Windows.Forms.TextBox()
		self._lblContract = System.Windows.Forms.Label()
		self._txtExchange = System.Windows.Forms.TextBox()
		self._txtProductType = System.Windows.Forms.TextBox()
		self._gboInstrumentMarketData = System.Windows.Forms.GroupBox()
		self._lblAskPrice = System.Windows.Forms.Label()
		self._txtAskPrice = System.Windows.Forms.TextBox()
		self._txtBidPrice = System.Windows.Forms.TextBox()
		self._lblChange = System.Windows.Forms.Label()
		self._txtChange = System.Windows.Forms.TextBox()
		self._lblBidPrice = System.Windows.Forms.Label()
		self._lblLastPrice = System.Windows.Forms.Label()
		self._txtLastPrice = System.Windows.Forms.TextBox()
		self._gboOrderEntry = System.Windows.Forms.GroupBox()
		self._label1 = System.Windows.Forms.Label()
		self._comboBoxOrderFeed = System.Windows.Forms.ComboBox()
		self._lblCustomer = System.Windows.Forms.Label()
		self._cboCustomer = System.Windows.Forms.ComboBox()
		self._txtOrderBook = System.Windows.Forms.TextBox()
		self._lblOrderType = System.Windows.Forms.Label()
		self._btnSell = System.Windows.Forms.Button()
		self._btnBuy = System.Windows.Forms.Button()
		self._lblStopPrice = System.Windows.Forms.Label()
		self._txtStopPrice = System.Windows.Forms.TextBox()
		self._cboOrderType = System.Windows.Forms.ComboBox()
		self._lblQuantity = System.Windows.Forms.Label()
		self._txtQuantity = System.Windows.Forms.TextBox()
		self._lblPrice = System.Windows.Forms.Label()
		self._txtPrice = System.Windows.Forms.TextBox()
		self._lblNotProduction = System.Windows.Forms.Label()
		self._lblWarning = System.Windows.Forms.Label()
		self._gboInstrumentInfo.SuspendLayout()
		self._gboInstrumentMarketData.SuspendLayout()
		self._gboOrderEntry.SuspendLayout()
		self.SuspendLayout()
		# 
		# sbaStatus
		# 
		self._sbaStatus.Location = System.Drawing.Point(0, 420)
		self._sbaStatus.Name = "sbaStatus"
		self._sbaStatus.Size = System.Drawing.Size(408, 22)
		self._sbaStatus.SizingGrip = False
		self._sbaStatus.TabIndex = 62
		self._sbaStatus.Text = "X_TRADER must be running to use this application."
		# 
		# mainMenu1
		# 
		self._mainMenu1.MenuItems.AddRange(Array[System.Windows.Forms.MenuItem]((self._mnuAbout)))
		# 
		# mnuAbout
		# 
		self._mnuAbout.Index = 0
		self._mnuAbout.Text = "About..."
		self._mnuAbout.Click += self._AboutMenuItem_Click
		# 
		# gboInstrumentInfo
		# 
		self._gboInstrumentInfo.Controls.Add(self._lblProductType)
		self._gboInstrumentInfo.Controls.Add(self._txtProduct)
		self._gboInstrumentInfo.Controls.Add(self._lblProduct)
		self._gboInstrumentInfo.Controls.Add(self._lblExchange)
		self._gboInstrumentInfo.Controls.Add(self._txtContract)
		self._gboInstrumentInfo.Controls.Add(self._lblContract)
		self._gboInstrumentInfo.Controls.Add(self._txtExchange)
		self._gboInstrumentInfo.Controls.Add(self._txtProductType)
		self._gboInstrumentInfo.FlatStyle = System.Windows.Forms.FlatStyle.System
		self._gboInstrumentInfo.Location = System.Drawing.Point(8, 56)
		self._gboInstrumentInfo.Name = "gboInstrumentInfo"
		self._gboInstrumentInfo.Size = System.Drawing.Size(216, 136)
		self._gboInstrumentInfo.TabIndex = 63
		self._gboInstrumentInfo.TabStop = False
		self._gboInstrumentInfo.Text = "Instrument Information"
		# 
		# lblProductType
		# 
		self._lblProductType.Location = System.Drawing.Point(8, 72)
		self._lblProductType.Name = "lblProductType"
		self._lblProductType.Size = System.Drawing.Size(80, 16)
		self._lblProductType.TabIndex = 38
		self._lblProductType.Text = "Product Type:"
		self._lblProductType.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# txtProduct
		# 
		self._txtProduct.Location = System.Drawing.Point(96, 48)
		self._txtProduct.Name = "txtProduct"
		self._txtProduct.Size = System.Drawing.Size(100, 20)
		self._txtProduct.TabIndex = 35
		# 
		# lblProduct
		# 
		self._lblProduct.Location = System.Drawing.Point(40, 48)
		self._lblProduct.Name = "lblProduct"
		self._lblProduct.Size = System.Drawing.Size(48, 16)
		self._lblProduct.TabIndex = 36
		self._lblProduct.Text = "Product:"
		self._lblProduct.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# lblExchange
		# 
		self._lblExchange.Location = System.Drawing.Point(24, 24)
		self._lblExchange.Name = "lblExchange"
		self._lblExchange.Size = System.Drawing.Size(64, 16)
		self._lblExchange.TabIndex = 34
		self._lblExchange.Text = "Market:"
		self._lblExchange.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# txtContract
		# 
		self._txtContract.Location = System.Drawing.Point(96, 96)
		self._txtContract.Name = "txtContract"
		self._txtContract.Size = System.Drawing.Size(100, 20)
		self._txtContract.TabIndex = 39
		# 
		# lblContract
		# 
		self._lblContract.Location = System.Drawing.Point(32, 96)
		self._lblContract.Name = "lblContract"
		self._lblContract.Size = System.Drawing.Size(56, 16)
		self._lblContract.TabIndex = 40
		self._lblContract.Text = "Contract:"
		self._lblContract.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# txtExchange
		# 
		self._txtExchange.Location = System.Drawing.Point(96, 24)
		self._txtExchange.Name = "txtExchange"
		self._txtExchange.Size = System.Drawing.Size(100, 20)
		self._txtExchange.TabIndex = 33
		# 
		# txtProductType
		# 
		self._txtProductType.Location = System.Drawing.Point(96, 72)
		self._txtProductType.Name = "txtProductType"
		self._txtProductType.Size = System.Drawing.Size(100, 20)
		self._txtProductType.TabIndex = 37
		# 
		# gboInstrumentMarketData
		# 
		self._gboInstrumentMarketData.Controls.Add(self._lblAskPrice)
		self._gboInstrumentMarketData.Controls.Add(self._txtAskPrice)
		self._gboInstrumentMarketData.Controls.Add(self._txtBidPrice)
		self._gboInstrumentMarketData.Controls.Add(self._lblChange)
		self._gboInstrumentMarketData.Controls.Add(self._txtChange)
		self._gboInstrumentMarketData.Controls.Add(self._lblBidPrice)
		self._gboInstrumentMarketData.Controls.Add(self._lblLastPrice)
		self._gboInstrumentMarketData.Controls.Add(self._txtLastPrice)
		self._gboInstrumentMarketData.FlatStyle = System.Windows.Forms.FlatStyle.System
		self._gboInstrumentMarketData.Location = System.Drawing.Point(232, 56)
		self._gboInstrumentMarketData.Name = "gboInstrumentMarketData"
		self._gboInstrumentMarketData.Size = System.Drawing.Size(168, 136)
		self._gboInstrumentMarketData.TabIndex = 64
		self._gboInstrumentMarketData.TabStop = False
		self._gboInstrumentMarketData.Text = "Instrument Market Data"
		# 
		# lblAskPrice
		# 
		self._lblAskPrice.Location = System.Drawing.Point(8, 48)
		self._lblAskPrice.Name = "lblAskPrice"
		self._lblAskPrice.Size = System.Drawing.Size(64, 16)
		self._lblAskPrice.TabIndex = 46
		self._lblAskPrice.Text = "Ask Price:"
		self._lblAskPrice.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# txtAskPrice
		# 
		self._txtAskPrice.Location = System.Drawing.Point(80, 48)
		self._txtAskPrice.Name = "txtAskPrice"
		self._txtAskPrice.Size = System.Drawing.Size(72, 20)
		self._txtAskPrice.TabIndex = 45
		# 
		# txtBidPrice
		# 
		self._txtBidPrice.Location = System.Drawing.Point(80, 24)
		self._txtBidPrice.Name = "txtBidPrice"
		self._txtBidPrice.Size = System.Drawing.Size(72, 20)
		self._txtBidPrice.TabIndex = 41
		# 
		# lblChange
		# 
		self._lblChange.Location = System.Drawing.Point(8, 96)
		self._lblChange.Name = "lblChange"
		self._lblChange.Size = System.Drawing.Size(64, 16)
		self._lblChange.TabIndex = 52
		self._lblChange.Text = "Change:"
		self._lblChange.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# txtChange
		# 
		self._txtChange.Location = System.Drawing.Point(80, 96)
		self._txtChange.Name = "txtChange"
		self._txtChange.Size = System.Drawing.Size(72, 20)
		self._txtChange.TabIndex = 51
		# 
		# lblBidPrice
		# 
		self._lblBidPrice.Location = System.Drawing.Point(8, 24)
		self._lblBidPrice.Name = "lblBidPrice"
		self._lblBidPrice.Size = System.Drawing.Size(64, 16)
		self._lblBidPrice.TabIndex = 42
		self._lblBidPrice.Text = "Bid Price:"
		self._lblBidPrice.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# lblLastPrice
		# 
		self._lblLastPrice.Location = System.Drawing.Point(8, 72)
		self._lblLastPrice.Name = "lblLastPrice"
		self._lblLastPrice.Size = System.Drawing.Size(64, 16)
		self._lblLastPrice.TabIndex = 50
		self._lblLastPrice.Text = "Last Price:"
		self._lblLastPrice.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# txtLastPrice
		# 
		self._txtLastPrice.Location = System.Drawing.Point(80, 72)
		self._txtLastPrice.Name = "txtLastPrice"
		self._txtLastPrice.Size = System.Drawing.Size(72, 20)
		self._txtLastPrice.TabIndex = 49
		# 
		# gboOrderEntry
		# 
		self._gboOrderEntry.Controls.Add(self._label1)
		self._gboOrderEntry.Controls.Add(self._comboBoxOrderFeed)
		self._gboOrderEntry.Controls.Add(self._lblCustomer)
		self._gboOrderEntry.Controls.Add(self._cboCustomer)
		self._gboOrderEntry.Controls.Add(self._txtOrderBook)
		self._gboOrderEntry.Controls.Add(self._lblOrderType)
		self._gboOrderEntry.Controls.Add(self._btnSell)
		self._gboOrderEntry.Controls.Add(self._btnBuy)
		self._gboOrderEntry.Controls.Add(self._lblStopPrice)
		self._gboOrderEntry.Controls.Add(self._txtStopPrice)
		self._gboOrderEntry.Controls.Add(self._cboOrderType)
		self._gboOrderEntry.Controls.Add(self._lblQuantity)
		self._gboOrderEntry.Controls.Add(self._txtQuantity)
		self._gboOrderEntry.Controls.Add(self._lblPrice)
		self._gboOrderEntry.Controls.Add(self._txtPrice)
		self._gboOrderEntry.FlatStyle = System.Windows.Forms.FlatStyle.System
		self._gboOrderEntry.Location = System.Drawing.Point(8, 200)
		self._gboOrderEntry.Name = "gboOrderEntry"
		self._gboOrderEntry.Size = System.Drawing.Size(392, 215)
		self._gboOrderEntry.TabIndex = 65
		self._gboOrderEntry.TabStop = False
		self._gboOrderEntry.Text = "Order Entry"
		# 
		# label1
		# 
		self._label1.Location = System.Drawing.Point(3, 51)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(69, 21)
		self._label1.TabIndex = 49
		self._label1.Text = "Order Feed:"
		self._label1.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# comboBoxOrderFeed
		# 
		self._comboBoxOrderFeed.DisplayMember = "Name"
		self._comboBoxOrderFeed.Enabled = False
		self._comboBoxOrderFeed.Items.AddRange(Array[Object](("Market", "Limit", "Stop Market", "Stop Limit")))
		self._comboBoxOrderFeed.Location = System.Drawing.Point(80, 51)
		self._comboBoxOrderFeed.Name = "comboBoxOrderFeed"
		self._comboBoxOrderFeed.Size = System.Drawing.Size(88, 21)
		self._comboBoxOrderFeed.TabIndex = 48
		# 
		# lblCustomer
		# 
		self._lblCustomer.Location = System.Drawing.Point(8, 24)
		self._lblCustomer.Name = "lblCustomer"
		self._lblCustomer.Size = System.Drawing.Size(64, 16)
		self._lblCustomer.TabIndex = 47
		self._lblCustomer.Text = "Customer:"
		self._lblCustomer.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# cboCustomer
		# 
		self._cboCustomer.DisplayMember = "Customer"
		self._cboCustomer.Enabled = False
		self._cboCustomer.Location = System.Drawing.Point(80, 24)
		self._cboCustomer.Name = "cboCustomer"
		self._cboCustomer.Size = System.Drawing.Size(88, 21)
		self._cboCustomer.TabIndex = 46
		# 
		# txtOrderBook
		# 
		self._txtOrderBook.Location = System.Drawing.Point(184, 24)
		self._txtOrderBook.Multiline = True
		self._txtOrderBook.Name = "txtOrderBook"
		self._txtOrderBook.ScrollBars = System.Windows.Forms.ScrollBars.Vertical
		self._txtOrderBook.Size = System.Drawing.Size(192, 181)
		self._txtOrderBook.TabIndex = 45
		# 
		# lblOrderType
		# 
		self._lblOrderType.Location = System.Drawing.Point(8, 78)
		self._lblOrderType.Name = "lblOrderType"
		self._lblOrderType.Size = System.Drawing.Size(64, 16)
		self._lblOrderType.TabIndex = 44
		self._lblOrderType.Text = "Order Type:"
		self._lblOrderType.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# btnSell
		# 
		self._btnSell.Enabled = False
		self._btnSell.FlatStyle = System.Windows.Forms.FlatStyle.System
		self._btnSell.Location = System.Drawing.Point(112, 182)
		self._btnSell.Name = "btnSell"
		self._btnSell.Size = System.Drawing.Size(56, 23)
		self._btnSell.TabIndex = 43
		self._btnSell.Text = "Sell"
		self._btnSell.Click += self._SellButton_Click
		# 
		# btnBuy
		# 
		self._btnBuy.Enabled = False
		self._btnBuy.FlatStyle = System.Windows.Forms.FlatStyle.System
		self._btnBuy.Location = System.Drawing.Point(56, 182)
		self._btnBuy.Name = "btnBuy"
		self._btnBuy.Size = System.Drawing.Size(56, 23)
		self._btnBuy.TabIndex = 42
		self._btnBuy.Text = "Buy"
		self._btnBuy.Click += self._BuyButton_Click
		# 
		# lblStopPrice
		# 
		self._lblStopPrice.Location = System.Drawing.Point(8, 150)
		self._lblStopPrice.Name = "lblStopPrice"
		self._lblStopPrice.Size = System.Drawing.Size(64, 16)
		self._lblStopPrice.TabIndex = 41
		self._lblStopPrice.Text = "Stop Price:"
		self._lblStopPrice.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# txtStopPrice
		# 
		self._txtStopPrice.Enabled = False
		self._txtStopPrice.Location = System.Drawing.Point(80, 150)
		self._txtStopPrice.Name = "txtStopPrice"
		self._txtStopPrice.Size = System.Drawing.Size(88, 20)
		self._txtStopPrice.TabIndex = 40
		# 
		# cboOrderType
		# 
		self._cboOrderType.Enabled = False
		self._cboOrderType.Items.AddRange(Array[Object](("Market", "Limit", "Stop Market", "Stop Limit")))
		self._cboOrderType.Location = System.Drawing.Point(80, 78)
		self._cboOrderType.Name = "cboOrderType"
		self._cboOrderType.Size = System.Drawing.Size(88, 21)
		self._cboOrderType.TabIndex = 39
		self._cboOrderType.SelectedIndexChanged += self._orderTypeComboBox_SelectedIndexChanged
		# 
		# lblQuantity
		# 
		self._lblQuantity.Location = System.Drawing.Point(8, 126)
		self._lblQuantity.Name = "lblQuantity"
		self._lblQuantity.Size = System.Drawing.Size(64, 16)
		self._lblQuantity.TabIndex = 38
		self._lblQuantity.Text = "Quantity:"
		self._lblQuantity.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# txtQuantity
		# 
		self._txtQuantity.Enabled = False
		self._txtQuantity.Location = System.Drawing.Point(80, 126)
		self._txtQuantity.Name = "txtQuantity"
		self._txtQuantity.Size = System.Drawing.Size(88, 20)
		self._txtQuantity.TabIndex = 37
		# 
		# lblPrice
		# 
		self._lblPrice.Location = System.Drawing.Point(8, 102)
		self._lblPrice.Name = "lblPrice"
		self._lblPrice.Size = System.Drawing.Size(64, 16)
		self._lblPrice.TabIndex = 36
		self._lblPrice.Text = "Price:"
		self._lblPrice.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# txtPrice
		# 
		self._txtPrice.Enabled = False
		self._txtPrice.Location = System.Drawing.Point(80, 102)
		self._txtPrice.Name = "txtPrice"
		self._txtPrice.Size = System.Drawing.Size(88, 20)
		self._txtPrice.TabIndex = 35
		# 
		# lblNotProduction
		# 
		self._lblNotProduction.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((0)))
		self._lblNotProduction.Location = System.Drawing.Point(8, 34)
		self._lblNotProduction.Name = "lblNotProduction"
		self._lblNotProduction.Size = System.Drawing.Size(392, 14)
		self._lblNotProduction.TabIndex = 67
		self._lblNotProduction.Text = "This sample is NOT to be used in production or during conformance testing."
		self._lblNotProduction.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# lblWarning
		# 
		self._lblWarning.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((0)))
		self._lblWarning.Location = System.Drawing.Point(8, 9)
		self._lblWarning.Name = "lblWarning"
		self._lblWarning.Size = System.Drawing.Size(392, 23)
		self._lblWarning.TabIndex = 66
		self._lblWarning.Text = "WARNING!"
		self._lblWarning.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# frmSubmitOrder
		# 
		self._AllowDrop = True
		self._AutoScaleBaseSize = System.Drawing.Size(5, 13)
		self._ClientSize = System.Drawing.Size(408, 442)
		self._Controls.Add(self._lblNotProduction)
		self._Controls.Add(self._lblWarning)
		self._Controls.Add(self._gboOrderEntry)
		self._Controls.Add(self._gboInstrumentMarketData)
		self._Controls.Add(self._gboInstrumentInfo)
		self._Controls.Add(self._sbaStatus)
		self._Enabled = False
		self._FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
		self._Menu = self._mainMenu1
		self._Name = "frmSubmitOrder"
		self._StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self._Text = "SubmitOrder"
		self._DragDrop += self._frmSubmitOrder_DragDrop
		self._DragOver += self._frmSubmitOrder_DragOver
		self._gboInstrumentInfo.ResumeLayout(False)
		self._gboInstrumentInfo.PerformLayout()
		self._gboInstrumentMarketData.ResumeLayout(False)
		self._gboInstrumentMarketData.PerformLayout()
		self._gboOrderEntry.ResumeLayout(False)
		self._gboOrderEntry.PerformLayout()
		self.ResumeLayout(False)

	def populateOrderFeedDropDown(self, instrument):
		""" <summary>
		 populate the OrderFeed drop down menu.
		 </summary>
		 <remarks>
		 comboBoxOrderFeed DisplayMember is set to Name to display the OrderFeed's Name property.
		 </remarks>
		 <param name="instrument">Instrument to find valid order feeds.</param>
		"""
		self._comboBoxOrderFeed.Items.Clear()
		enumerator = instrument.GetValidOrderFeeds().GetEnumerator()
		while enumerator.MoveNext():
			orderFeed = enumerator.Current
			self._comboBoxOrderFeed.Items.Add(orderFeed)

	def m_customerDefaultsSubscription_CustomerDefaultsChanged(self, sender, e):
		""" <summary>
		 CustomerDefaultsChanged subscription callback.
		 Update the Customer combo box.
		 </summary>
		"""
		self._cboCustomer.Items.Clear()
		cds = sender
		enumerator = cds.CustomerDefaults.GetEnumerator()
		while enumerator.MoveNext():
			entry = enumerator.Current
			self._cboCustomer.Items.Add(entry)

	def orderTypeComboBox_SelectedIndexChanged(self, sender, e):
		""" <summary>
		 This function enables and disables the appropriate
		 text boxes on the user interface.
		 </summary>
		 <param name="sender">Object which fires the method</param>
		 <param name="e">Event arguments of the callback</param>
		"""
		if self._cboOrderType.SelectedIndex == 2 or self._cboOrderType.SelectedIndex == 3:
			# Enable the stop price text box if the selected order type is stop limit or stop market.
			self._txtStopPrice.Enabled = True
		else:
			# Clear and disable the stop price text box if not stop limit or stop market.
			self._txtStopPrice.Clear()
			self._txtStopPrice.Enabled = False
		if self._cboOrderType.SelectedIndex == 0 or self._cboOrderType.SelectedIndex == 2:
			# Clear and disable the price text box if the selected order type is market or stop market.
			self._txtPrice.Clear()
			self._txtPrice.Enabled = False
		else:
			# Enable the price text box if the if the selected order type is limit or stop limit.
			self._txtPrice.Enabled = True

	def BuyButton_Click(self, sender, e):
		""" <summary>
		 This function is called when the user clicks the buy button.
		 </summary>
		 <param name="sender">Object which fires the method</param>
		 <param name="e">Event arguments of the callback</param>
		"""
		# Call the SendOrder function with a Buy request.
		self.SendOrder(BuySell.Buy)

	def SellButton_Click(self, sender, e):
		""" <summary>
		 This function is called when the user clicks the sell button.
		 </summary>
		 <param name="sender">Object which fires the method</param>
		 <param name="e">Event arguments of the callback</param>
		"""
		# Call the SendOrder function with a Sell request.
		self.SendOrder(BuySell.Sell)

	def SendOrder(self, buySell):
		""" <summary>
		 This function sets up the OrderProfile and submits
		 the order using the InstrumentTradeSubscription SendOrder method.
		 </summary>
		 <param name="buySell">The side of the market to place the order on.</param>
		"""
		try:
			orderFeed = self._comboBoxOrderFeed.SelectedItem
			customer = self._cboCustomer.SelectedItem
			orderProfile = OrderProfile(orderFeed, self._m_instrumentTradeSubscription.Instrument, customer.Customer)
			# Set for Buy or Sell.
			orderProfile.BuySell = buySell
			# Set the quantity.
			orderProfile.QuantityToWork = Quantity.FromString(self._m_instrumentTradeSubscription.Instrument, self._txtQuantity.Text)
			# Determine which Order Type is selected.
			if self._cboOrderType.SelectedIndex == 0: # Market Order
				# Set the order type to "Market" for a market order.
				orderProfile.OrderType = OrderType.Market
			elif self._cboOrderType.SelectedIndex == 1: # Limit Order
				# Set the order type to "Limit" for a limit order.
				orderProfile.OrderType = OrderType.Limit
				# Set the limit order price.
				orderProfile.LimitPrice = Price.FromString(self._m_instrumentTradeSubscription.Instrument, self._txtPrice.Text)
			elif self._cboOrderType.SelectedIndex == 2: # Stop Market Order
				# Set the order type to "Market" for a market order.
				orderProfile.OrderType = OrderType.Market
				# Set the order modifiers to "Stop" for a stop order.
				orderProfile.Modifiers = OrderModifiers.Stop
				# Set the stop price.
				orderProfile.StopPrice = Price.FromString(self._m_instrumentTradeSubscription.Instrument, self._txtStopPrice.Text)
			elif self._cboOrderType.SelectedIndex == 3: # Stop Limit Order
				# Set the order type to "Limit" for a limit order.
				orderProfile.OrderType = OrderType.Limit
				# Set the order modifiers to "Stop" for a stop order.
				orderProfile.Modifiers = OrderModifiers.Stop
				# Set the limit order price.
				orderProfile.LimitPrice = Price.FromString(self._m_instrumentTradeSubscription.Instrument, self._txtPrice.Text)
				# Set the stop price.
				orderProfile.StopPrice = Price.FromString(self._m_instrumentTradeSubscription.Instrument, self._txtStopPrice.Text)
			# Send the order.
			self._m_instrumentTradeSubscription.SendOrder(orderProfile)
			# Update the GUI.
			self._txtOrderBook.Text += 
		except Exception, err:
			MessageBox.Show(err.Message)
		finally:

	def m_priceSubscription_FieldsUpdated(self, sender, e):
		""" <summary>
		 PriceSubscription FieldsUpdated event.
		 </summary>
		"""
		if e.Error == None:
			if e.UpdateType == UpdateType.Snapshot:
				self.updatePrices(e.Fields)
			elif e.UpdateType == UpdateType.Update:
				self.updatePrices(e.Fields)
		else:
			Console.WriteLine(String.Format("PriceSubscription FieldsUpdated Error: {0}", e.Error.Message))

	def updatePrices(self, fields):
		""" <summary>
		 Update the price information.
		 </summary>
		 <param name="fields">PriceSubscriptionFields</param>
		"""
		self._txtBidPrice.Text = fields.GetBestBidPriceField().Value.ToString()
		self._txtAskPrice.Text = fields.GetBestAskPriceField().Value.ToString()
		self._txtLastPrice.Text = fields.GetLastTradedPriceField().Value.ToString()
		self._txtChange.Text = fields.GetNetChangeField().Value.ToString()

	def m_instrumentTradeSubscription_OrderRejected(self, sender, e):
		""" <summary>
		 OrderRejected InstrumentTradeSubscription callback.
		 </summary>
		 <param name="sender">Sender (InstrumentTradeSubscription)</param>
		 <param name="e">OrderRejectedEventArgs</param>
		"""
		self._txtOrderBook.Text += 

	def m_instrumentTradeSubscription_OrderAdded(self, sender, e):
		""" <summary>
		 OrderAdded InstrumentTradeSubscription callback.
		 </summary>
		 <param name="sender">Sender (InstrumentTradeSubscription)</param>
		 <param name="e">OrderAddedEventArgs</param>
		"""
		self._txtOrderBook.Text += 

	def FindInstrument(self, keys):
		""" <summary>
		 Function to find a list of InstrumentKeys.
		 </summary>
		 <param name="keys">List of InstrumentKeys.</param>
		"""
		enumerator = keys.GetEnumerator()
		while enumerator.MoveNext():
			key = enumerator.Current
			# Update the Status Bar text.
			self.UpdateStatusBar(String.Format("TT API FindInstrument {0}", key.ToString()))
			instrRequest = InstrumentLookupSubscription(self._m_TTAPI.Session, Dispatcher.Current, key)
			instrRequest.Update += self.instrRequest_Completed
			instrRequest.Tag = key.ToString()
			instrRequest.Start()
			# Only allow the first instrument.
			break

	def instrRequest_Completed(self, sender, e):
		""" <summary>
		 Instrument request completed event.
		 </summary>
		"""
		if e.IsFinal and e.Instrument != None:
			try:
				self.UpdateStatusBar(String.Format("TT API FindInstrument {0}", e.Instrument.Name))
				self.instrumentFound(e.Instrument)
			except Exception, err:
				self.UpdateStatusBar(String.Format("TT API FindInstrument Exception: {0}", err.Message))
			finally:
		elif e.IsFinal:
			self.UpdateStatusBar(String.Format("TT API FindInstrument Instrument Not Found: {0}", e.Error))
		else:
			self.UpdateStatusBar(String.Format("TT API FindInstrument Instrument Not Found: (Still Searching) {0}", e.Error))

	def instrumentFound(self, instrument):
		""" <summary>
		 Create subscriptions and update the GUI.
		 </summary>
		 <param name="instrument">Instrument to create subscriptions with.</param>
		"""
		self._txtExchange.Text = instrument.Key.MarketKey.Name
		self._txtProduct.Text = instrument.Key.ProductKey.Name
		self._txtProductType.Text = instrument.Key.ProductKey.Type.Name
		self._txtContract.Text = instrument.Name
		self._m_priceSubscription = PriceSubscription(instrument, Dispatcher.Current)
		self._m_priceSubscription.FieldsUpdated += self.m_priceSubscription_FieldsUpdated
		self._m_priceSubscription.Start()
		self._m_instrumentTradeSubscription = InstrumentTradeSubscription(self._m_TTAPI.Session, Dispatcher.Current, instrument)
		self._m_instrumentTradeSubscription.OrderAdded += self.m_instrumentTradeSubscription_OrderAdded
		self._m_instrumentTradeSubscription.OrderRejected += self.m_instrumentTradeSubscription_OrderRejected
		self._m_instrumentTradeSubscription.Start()
		self.populateOrderFeedDropDown(instrument)
		# Enable the user interface items.
		self._txtQuantity.Enabled = True
		self._cboOrderType.Enabled = True
		self._comboBoxOrderFeed.Enabled = True
		self._cboCustomer.Enabled = True
		self._btnBuy.Enabled = True
		self._btnSell.Enabled = True

	def frmSubmitOrder_DragDrop(self, sender, e):
		""" <summary>
		 Form drag and drop event handler.
		 The form must enable "AllowDrop" for these events to fire.
		 </summary>
		"""
		if e.Data.HasInstrumentKeys():
			self.FindInstrument(e.Data.GetInstrumentKeys())

	def frmSubmitOrder_DragOver(self, sender, e):
		""" <summary>
		 Form drag over event handler.
		 The form must enable "AllowDrop" for these events to fire.
		 </summary>
		"""
		if e.Data.HasInstrumentKeys():
			e.Effect = DragDropEffects.Copy
 # <summary>
	# Update the status bar and write the message to the console in a thread safe way.
	# </summary>
	# <param name="message">Message to update the status bar with.</param>
	def UpdateStatusBar(self, message):
		if self._InvokeRequired:
			statCB = UpdateStatusBarCallback(UpdateStatusBar)
			self.Invoke(statCB, Array[Object]((message)))
		else:
			# Update the status bar.
			self._sbaStatus.Text = message
			# Also write this message to the console.
			Console.WriteLine(message)

	def AboutMenuItem_Click(self, sender, e):
		""" <summary>
		 Display the About dialog box.
		 </summary>
		 <param name="sender">Object which fires the method</param>
		 <param name="e">Event arguments of the callback</param>
		"""
		aboutForm = AboutDTS()
		aboutForm.ShowDialog(self)
