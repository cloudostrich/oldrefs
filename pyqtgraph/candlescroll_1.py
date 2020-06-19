# -*- coding: utf-8 -*-

"""
Demonstrate creation of a custom graphic (a candlestick plot)

"""
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
import random


class CandleStick(pg.GraphicsObject):
    '''Create a subclass of GraphicsObject. The only required methods
    are paint() and boundingRect().(see QGraphicsItem documentation)'''
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.flagHasData = False

    def set_data(self, data):
        self.data = data  ## data must have fields: time, open, close, min, max
        self.flagHasData = True
        self.generatePicture()
        self.informViewBoundsChanged()
        self.update() #to enable update after zoom in/out
        

    def generatePicture(self):
        ''' pre-computing a QPicture object allows paint() to run
        much more quickly, rather than re-drawing the shapes every time.'''
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, opn, high, low, close) in self.data:
            p.drawLine(QtCore.QPointF(t, low), QtCore.QPointF(t, high))
            if opn > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QtCore.QRectF(t-w, opn, w*2, close-opn))
        p.end()

    def paint(self, p, *args):
        if self.flagHasData:
            p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        '''boundingRect _must_ indicate the entire area that will be
        drawn on or else we will get artifacts and possibly crashing.
        (in this case, QPicture does all the work of computing the
        bounding rect for us)'''
        return QtCore.QRectF(self.picture.boundingRect())

mytitle = 'WAKAYAKINIKU'
app = QtGui.QApplication([])
#pg.setConfigOptions(antialias=True) #antialising for prettier plots?
data = [  ## fields are (time, opn, high, low, close).
    [1., 10, 15, 5, 13],
    [2., 13, 20, 9, 17],
    [3., 17, 23, 11, 14],
    [4., 14, 19, 5, 15],
    [5., 15, 22, 8, 9],
    [6., 9, 16, 8, 15],
    [7., 10, 15, 5, 13],
    [8., 13, 20, 9, 17],
    [9., 17, 23, 11, 14],
    [10., 14, 19, 5, 15],
    [11., 15, 22, 8, 9],
]

mycandle = CandleStick() #instantiate a candlestick object
mycandle.set_data(data) # reference the data

#plt = pg.PlotItem.plot(title=mytitle)
plt = pg.plot(title=mytitle) 
plt.addItem(mycandle)

#plt.setXRange(data[-5][0],data[-1][0]+1)
plt.setWindowIcon(QtGui.QIcon("icon-mongol.jpg")) # no icon??
plt.showAxis('right')  # set attributes of chart
plt.hideAxis('left')
plt.showGrid(x=True,y=True,alpha=1.0)
plt.addLine(y=10)
#plt.setAutoPan(x=True) # my try

def update():
    global mycandle, data
    data_len = len(data)
    rand = random.randint(0, len(data)-1)
    new_bar = data[rand][:]
    new_bar[0] = data_len + 1
    data.append(new_bar)
    #ptr += 1
    mycandle.set_data(data)
    mycandle.setX
    a = mycandle.getViewBox()  # this part scroll candlestick to updates
    a.setXRange(data[-10][0],data[-1][0]+1)
    print(data[-10][0], data[-1][0]+1)
    #mycandle.setPos(-ptr,0)
    app.processEvents()  ## force complete redraw for every plot

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.instance().exec_()
