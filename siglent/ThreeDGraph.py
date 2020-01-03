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
GAIN = 1


class Graph:
    """Create a window in which to display the 3d display

    The window contains two grids and the 3d display.  The axes are
    time (history of former traces) , time (for a given trace) and
    amplitude of the points in the trace.  The grids are on the
    (history)time-amplitude and (history) time-time axes.  No grid is
    generated for the (trace) time-amplitude axes so as not to occlude
    the line-of-site of the display


    Args: 
        rows (int): Defines the size of the waterfall in rows.  This
                    value represents the numper of points per trace.

        cols (int): Defines the size of the waterfall in columns.  This
                    value represents the depth of the storage.  This
                    is the number of traces to display

    Keyword args:
        title (str): The name of the waterfall window.  Defaults to
                     *3d Waterfall Display*

        distance (int): The inital distance of the observer from the
                        3D display

    """

    import pyqtgraph.opengl as gl
    import pyqtgraph as pg
    import numpy as np

    def __init__(self, rows, cols, title="3D Waterfall Display",
                 distance=50):
        log.logger.debug(f"Instantiating 3D Display. rows={rows}, cols={cols}")

        self.rows = rows
        self.cols = cols
        self.amplitude = self.np.zeros((self.rows, self.cols))

        self.xData = self.np.linspace(-10,
                                      10,
                                      self.cols).reshape(1, self.cols)
        self.time = self.np.linspace(-9,
                                     9,
                                     self.rows).reshape(self.rows, 1)
        self.plotItem = self.gl.GLSurfacePlotItem(
            x=self.time[:, 0],
            y=self.xData[0, :],
            shader='heightColor',
            computeNormals=False,
            smooth=False)
#        self.plotItem.shader()['colorMap'] = self.np.array(
#            [0.0, 0.0, 0.0,  0.0,
#             1.1, 1, 1, 1])
        self.plotItem.shader()['colorMap'] = self.np.array(
            [0.2, 2, 0.5,
             0.2, 1, 1,
             0.2, 0, 2])
        

        # Create the window with two orthogonal grids and an axis indicator.
        # ... and add our Plot Item.

        gridxy = self.gl.GLGridItem()  # Time Frequency Plane
        gridzy = self.gl.GLGridItem()  # Amplitude Time Plane
        axis = self.gl.GLAxisItem()
        self.win = self.gl.GLViewWidget()

        gridxy.scale(1, 1, 1)

        gridzy.scale(1, 1, 10)
        gridzy.rotate(90, 1, 0, 0)
        gridzy.translate(0, -10, 10)

        axis.setSize(-20, 20, 20)
        axis.translate(9.01, -9.99, 0.01)

        self.win.setWindowTitle(title)
        self.win.setCameraPosition(distance=distance)
        self.win.addItem(self.plotItem)
        self.win.addItem(gridxy)
        self.win.addItem(gridzy)
        self.win.addItem(axis)
        self.win.show()

    def update(self, data):
        """ Obtain next chunk of data, update the waterfall display"""
        # data = abs(data[:self.cols])*self.deEmphasis[:self.cols]
        self.amplitude =  self.np.vstack((
            self.amplitude[1:], list(map(lambda x: x*GAIN, data[1]))))
        # z = self.amplitude[:-self.latency, :]
        self.plotItem.setData(z=self.amplitude)
