#!/usr/bin/python 
# -*- coding: utf-8 -*- 

import xlrd 

book = xlrd.open_workbook("python_spreadsheet.xls") 

for sheet_name in book.sheet_names(): 
   sheet = book.sheet_by_name(sheet_name) 
   print sheet.row_values(0)[0]