# for getting the stupid OI from tocom site
import urllib
import csv

def get_Csv(oiDate1):
    a = urllib.urlretrieve('http://www.tocom.or.jp/data/yakujou/1181_' + oiDate1 + '.csv',r'D:\pythonstuff\sqlite3stuff\tocomoi.csv')

def read_Csv(oiDate):
    oi1 = csv.reader(open('tocomoi.csv','rb'))
    oi2 = []
    for i in oi1:
        if i[0] == oiDate:
            oi2.append(int(i[-1]))
    return oi2
    print(oi2)
