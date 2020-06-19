# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:05:31 2017

@author: User
"""

import clr
import System

print(System.Environment.Version)

clr.AddReference('C:\\tt\\ttapi\\bin\\TradingTechnologies.TTAPI')

import TradingTechnologies.TTAPI as ttapi

help(ttapi)

ttapi.XTraderModeTTAPI
print(ttapi.XTraderModeTTAPI)
ttapi.XTraderModeTTAPI.Start()
ttapi.XTraderModeTTAPI.StartFillFeed
ttapi.XTraderModeTTAPI.StartFillFeed()
help(ttapi.Dispatcher)
disp = ttapi.Dispatcher.AttachWorkerDispatcher()
disp.BeginInvoke(new Action(Init))
disp.BeginInvoke(Action(Init))
disp.BeginInvoke(Action)
disp.BeginInvoke()
disp = ttapi.Dispatcher.AttachUIDispatcher()
h=ttapi.ApiInitializeHandler()
h=ttapi.ApiInitializeHandler(ttapi.FillUpdateFlag)
ttapi.XTraderModeTTAPIOptions.StartOrderFillFeed()
ttapi.XTraderModeTTAPI.ConnectionStatusUpdate()
ttapi.XTraderModeTTAPI.CreateXTraderModeTTAPI(disp,h)
ttapi.XTraderModeTTAPI.ConnectionStatusUpdate()
star = ttapi.XTraderModeTTAPI.CreateXTraderModeTTAPI(disp,h)
star = ttapi.XTraderModeTTAPI.Start()
ttapi.Session()
ttapi.XTraderModeTTAPI.ConnectionStatusUpdate()
ttapi.XTraderModeTTAPI.m_UserName()
ttapi.XTraderModeTTAPI.Shutdown()