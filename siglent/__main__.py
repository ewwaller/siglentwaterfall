"""
Display a 3D waterfall of the trace data read from a Siglent SDS
1204x-e oscilloscope
"""

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
import siglent.background
import siglent.ThreeDGraph as Graph
import siglent.TwoDGraph as twoD
import click
import time
import multiprocessing as mp
import signal
from pyqtgraph.Qt import QtGui, QtCore
import sys
import numpy

UPDATE_PERIOD = 0.010 #seconds

def set_log(ctc, param, value):
    log.setLog("WARNING" if value == 0
               else "INFO" if value == 1
               else "DEBUG")


@click.command()
@click.option('--rows', '-r', type=click.INT, default=512,
              help="Rows in waterfall display (number of traces)")
@click.option('--cols', '-c', type=click.INT, default=512,
              help="columns in waterfall display (samples/trace)")
@click.option('--waterfall', is_flag=True, default=False,
              help="Show the 3D Display")
@click.option('--channel', type=click.STRING, default='C1',
              help="Scope channel to capture (default=C1)")
@click.option('--name', '-n', type=click.STRING, required=True,
              help="VISA Address of the oscilloscope")
@click.option('-v', '--verbose', count=True, callback=set_log,
              is_eager=True, expose_value=False,
              help="Be verbose.  Invoke twice for more verbosity")
@click.option('-L', '--log-file', default=None,
              type=click.Path(),
              help="Log file Name.")
@click.option('--timeout', '-t', type=click.INT, default=0,
              help="Foreground process timeout in seconds (debug only)")
@click.option('--bgtimeout', '-b', type=click.INT, default=0,
              help="Background process timeout in seconds (debug only)")
def main(timeout, bgtimeout, rows, cols, waterfall,
         channel, name, log_file):
    """ Siglent

    Display a YT display and (optionally) a waterfall display of scope
    traces obtained from an SDS 1204X-E oscilloscope.
    """

    if log_file:
        log.setLogFile(log_file)
    background_conn, foreground_conn = mp.Pipe()
    theProcess = mp.Process(target=siglent.background.main,
                            args=(cols, bgtimeout,
                                  name, channel,
                                  background_conn,))
    startTime = time.time()
    theWaterfallGraph = None
    theYTGraph = None

    def sigint_handler(*args):
        """sigint_Handler: Kill background process if Ctrl-C is caught

        Send a message to the background process that will cause it to
        stop.  Once the background process stops, the forground
        process will exit.
        """

        log.logger.debug("Caught Keyboard Interrupt. "
                         "Killing Background process")
        foreground_conn.send(siglent.background.Message('halt'))

    def update():
        """ Update the displays

        Check the queue for messages from the background process.  If
        it is a scope trace record, update the 2D display and
        (optionally) the 3D display.

        """
        if not theProcess.is_alive():
            app.quit()
        if (timeout > 0
           and (time.time() - startTime) > timeout):
            log.logger.info("Posting Halt message to background process")
            foreground_conn.send(siglent.background.Message('halt'))
        while foreground_conn.poll():
            message = foreground_conn.recv()
            if type(message) == siglent.background.Message:
                log.logger.info(f"Received Command was {message.command}")
            elif type(message) == tuple:
                # message is next chunk data
                # update the waterfall display
                theYTGraph.update(message)
                if waterfall:
                    theWaterfallGraph.update(message)
            else:
                log.logger.warn(f"Unknown message type: {type(message)}")

    # If we receive a SIGINT (Ctrl -C) respond by killing background
    # process.  That will eventually lead to this main function doing
    # an orderly exit.

    signal.signal(signal.SIGINT, sigint_handler)
    log.logger.info('Starting background process')
    theProcess.start()

    app = QtGui.QApplication([])
    theYTGraph = twoD.Graph(cols)
    if waterfall:
        theWaterfallGraph = Graph.Graph(rows, cols)

    # Set up a recurring callback that is bound to the update method of our
    # Waterfall

    log.logger.info("Starting Timer. Timeout=%imS" % (UPDATE_PERIOD))

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(UPDATE_PERIOD)

    # Start the Qt main loop.  This never exits by itself.  If the user kills
    # the window or enters a Ctrl-C, the app will exit.

    log.logger.info('Starting main loop')

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

    log.logger.info("Application Exited")

    # Check to see if the app died leaving the background task running
    # if so, terminate the background task

    if theProcess.is_alive():
        foreground_conn.send(siglent.background.Message('halt'))

    log.logger.info("Done")


if __name__ == "__main__":
    main()
