import urllib2
from bs4 import BeautifulSoup
import sqlite3
import datetime
import tocomOI

#get soup of website with url given
def get_Site(sitename):
    url_Name = sitename
    opened_Url = urllib2.urlopen(url_Name)
    souped_Url = BeautifulSoup(opened_Url)
    return souped_Url

#get date and time
def get_Time(soupUrl):
    dateTime = soupUrl.body.find("table", {"class":"nostyle"}).get_text()
    dateTime = dateTime[49:67].encode()
    timE = dateTime[62:67].encode()
    return dateTime

#Better way to get date and time?
def get_Time2():
    now = datetime.datetime.today()
    return now

def write_Data(table_Nam, cDate, cCnum, cMonth, cOpen = None, cHigh = None, cLow = None, cClose = None, cSettle = None, cVol = None, cOI= None):
    with con:
        cur = con.cursor()
        dataIn = (cDate, cCnum, cMonth, cOpen, cHigh, cLow, cClose, cSettle, cVol, cOI)
        #print dataIn
        cur.execute("""INSERT INTO """ + table_Nam +"""(Date, Cnum, Month, Open, High,
                        Low, Close, Settle, Vol, OI) VALUES (?,?,?,?,?,?,?,?,?,?)""",(dataIn))
        con.commit()
        
#get each data table by table num, extract the string data and write to db file
def get_Data(soupUrl, table_Num, table_Nam,dateTime,numOI):
    priceTable = soupUrl.body.find_all("table",{"class":None})
    rows = priceTable[table_Num].find_all('tr')
    del rows[0]
    del rows[-1]
    cCnum = 0
    for row in rows:
        cCnum += 1
        cells = row.find_all('td')
        cOI = numOI[cCnum-1]
        cDate = dateTime
        cMonth = cells[0].get_text()
        #Last_settle = float(cells[1].get_text())
        try:
            cOpen = float(cells[2].get_text())
        except ValueError:
            cOpen = None

        try:
            cHigh = float(cells[3].get_text())
        except ValueError:
            cHigh = None

        try:
            cLow = float(cells[4].get_text())
        except ValueError:
            cLow = None

        try:
            cClose = float(cells[5].get_text())
        except ValueError:
            cClose = None
        #Change = float(cells[6].get_text())
        try:
            cVol = int(cells[7].get_text().replace(',',''))
        except ValueError:
            cVol = None

        try:
            cSettle = float(cells[8].get_text())
        except ValueError:
            cSettle = None
            
        write_Data(table_Nam, cDate, cCnum, cMonth, cOpen, cHigh, cLow, cClose, cSettle, cVol, cOI)

#def get_Daily():
    
def main():
    urlP = 'http://www.tocom.or.jp/souba/rubber/?chart=off'
    soupP = get_Site(urlP)
    dateTime = datetime.datetime.today()
    oiDate = str(datetime.datetime.today())
    print oiDate
    oiDate1 = oiDate[:7]
    print oiDate1
    oiDate = oiDate[:4] + oiDate[5:7] + oiDate[8:10]
    print oiDate
    tocomOI.get_Csv(oiDate1)
    numOI = tocomOI.read_Csv(oiDate)
    print numOI
    get_Data(soupP, 0, 'Night_Session', dateTime,numOI)
    get_Data(soupP, 2, 'Day_Session', dateTime,numOI)

con = sqlite3.connect('tocomtest4.db')
main()
con.close()
