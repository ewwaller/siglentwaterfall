# This program is licensed under the MIT license.
#
# Copyright (c) 2020 Eric Waller
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from siglent import log

class Graph:
    """Create a window in which to display the YT display

    The window contains two grids and the YT display.  The axes are
    time, and amplitude.

    Args:
        rows (int): Defines the horizontal size of plot in samples.

    Keyword args:
           title (str):  The name of the window. Defaults to *YT Display*

    """

    import pyqtgraph.opengl as gl
    import pyqtgraph as pg
    import numpy as np

    def __init__(self, rows, title="YT Display"):
        log.logger.debug(f"Instantiating YT Display. rows={rows}")

        self.rows = rows

        self.win = self.pg.GraphicsWindow(title=title)
        self.plotItem = self.win.addPlot(title="YT Plot")
        self.plotItem.showGrid(x=True, y=True)
        self.curve = self.plotItem.plot(pen='y')

        self.win.setWindowTitle(title)
        self.win.addItem(self.plotItem)
        self.win.show()
        self.firstPassFlag = True

    def update(self, data):
        """ Obtain next chunk of data, update the waterfall display"""
        self.curve.setData(data[0], data[1])
        if self.firstPassFlag:
            # stop auto-scaling after the first data set is plotted
            self.plotItem.enableAutoRange('y', False)
            self.firstPassFlag = False
