# Demo of a "tool" for pyqtgraph that, when attached to a plot item it adds a menu
# action that, when toggled, checks for new data periodically and auto pans the X axis.
# The new-data-checking period is dynamically adjusted depending on the range being 
# displayed
# 
# Snippet adapted from the taurus_pyqtgraph.autopantool module to be used without taurus.
# See: 
# https://github.com/taurus-org/taurus_pyqtgraph/blob/master/taurus_pyqtgraph/autopantool.py


#from PyQt4 import QtGui, QtCore
from pyqtgraph import QtGui, QtCore


class XAutoPanTool(QtGui.QAction):
    """
    A tool that provides the "AutoPan" for the X axis of a plot
    (aka "oscilloscope mode"). It is implemented as an Action, and provides a
    method to attach it to a :class:`pyqtgraph.PlotItem` (which adds an action
    to the X Axis context menu) 
    """

    def __init__(self, parent=None):
        QtGui.QAction.__init__(self, 'Auto Pan', parent)
        self.setCheckable(True)
        self.toggled.connect(self._onToggled)
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.updateRange)
        self._originalXAutoRange = None
        self._viewBox = None
        self._XactionMenu = None
        self._scrollStep = 0.2

    def attachToPlotItem(self, plot_item):
        """Use this method to add this tool to a plot
        :param plot_item: (PlotItem)
        """
        self._viewBox = plot_item.getViewBox()
        self._addToMenu(self._viewBox.menu)
        self._originalXAutoRange = self._viewBox.autoRangeEnabled()[0]
        self._viewBox.sigXRangeChanged.connect(self._onXRangeChanged)

    def _addToMenu(self, menu):
        for m in menu.axes:
            if m.title() == 'X Axis':
                x_menu = m
                self._XactionMenu = x_menu.actions()[0]
                x_menu.insertAction(self._XactionMenu, self)
                self.setParent(menu)

    def _onToggled(self, checked):
        if checked:
            self._originalXAutoRange = self._viewBox.autoRangeEnabled()[0]
            self._viewBox.enableAutoRange(x=False)

            axisXrange = self._viewBox.state['viewRange'][0]
            x_range = axisXrange[1] - axisXrange[0]

            t = int(x_range/10.)*1000
            t = min(3000, t)
            t = max(50, t)
            self._timer.start(t)
        else:
            self._timer.stop()
            self._viewBox.enableAutoRange(x=self._originalXAutoRange)

        self._XactionMenu.setEnabled(not checked)

    def _onXRangeChanged(self):
        self.setChecked(False)
        print('xrangecheck')

    def updateRange(self):
        """Pans the x axis (change the viewbox range maintaining width but
        ensuring that the right-most point is shown
        """
        if len(self._viewBox.addedItems) < 1:
            self._timer.stop()

        children_bounds = self._viewBox.childrenBounds()
        _, boundMax = children_bounds[0]

        axis_X_range, _ = self._viewBox.state['viewRange']

        x_range = axis_X_range[1] - axis_X_range[0]

        if boundMax > axis_X_range[1] or boundMax < axis_X_range[0]:
            x_min = boundMax - axis_X_range[1]
            x_max = boundMax - axis_X_range[0]
            step = 1 + x_min

            self._viewBox.sigXRangeChanged.disconnect(self._onXRangeChanged)
            self._viewBox.setXRange(axis_X_range[0]+step, axis_X_range[1]+step,
                                    padding=0.0, update=False)
            self._viewBox.sigXRangeChanged.connect(self._onXRangeChanged)



if __name__ == '__main__':
    import sys
    import numpy as np
    import pyqtgraph as pg

    app = QtGui.QApplication([])

    # use a standard Plot
    w = pg.PlotWidget()

    # add the XAutoPanTool
    autopan = XAutoPanTool()
    autopan.attachToPlotItem(w.getPlotItem())

    # add a curve that appends a new point every 500ms
    c = pg.PlotDataItem(symbol='x')
    idx = 40
    max_points = 10000
    xdata = np.arange(max_points)
    ydata = np.random.rand(max_points)
    c.setData(xdata[:idx], ydata[:idx])

    def addPoint():
        global idx
        idx += 1
        c.setData(xdata[:idx], ydata[:idx])
        print(autopan.isChecked(), idx)

    t = QtCore.QTimer()
    t.timeout.connect(addPoint)
    t.start(1000)

    w.addItem(c)

    # enable the AutoPan (same as checking "Auto Pan" in Context menu -> X Axis)
    autopan.toggle()

    # go
    w.show()

sys.exit(app.exec_())
