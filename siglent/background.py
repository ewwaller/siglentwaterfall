"""
Generate a stream of vectors read from a siglent oscilloscope
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
import time
import threading
import pyvisa
import signal


class Message:
    def __init__(self, command, **kwargs):
        self.command = command
        for key, value in kwargs:
            setattr(self, key, value)


class ScopeInitializationError(Exception):
    pass


class Acquire:
    """Acquire traces from the oscilloscope

    This class sets up the oscilloscope, then reads data from it
    continuously, posting those trace information to a queue that is
    processed by the main program.  This code is run in a multiprocess
    environment allowing it to run independently of the main program.
    Hopefully, it runs on its own core.

    Args:
        address (str): The *visa* address of the instrument

        channel (str): The channel to read from the scope.  Defaults
                       to 'C1'.  Values can be *C1, C2, C3, C4* or *math*

        cols (int):  The number of points to place in each vector.
                     This controls the *skip factor* in the waveform
                     setup. This decimates the 14K (or more) points in
                     the scope memory down to a manaeable number of
                     points

    """
    traceinfo = [
            {'name': 'vdiv', 'command': ':VDIV?', 'chars': 18,
             'minChars': None, 'payloadLocation': (8, -2)},
            {'name': 'tdiv', 'command': 'TDIV?', 'chars': 15,
             'minChars': 18, 'payloadLocation': (5, -2),
             'noChannelPrefix': True},
            {'name': 'sampleRate', 'command': 'SARA?', 'chars': 18,
             'minChars': 18, 'payloadLocation': (5, -5),
             'noChannelPrefix': True},
            {'name': 'offset', 'command': ':OFST?', 'chars': 19,
             'minChars': 18, 'payloadLocation': (8, -2)},
            {'name': 'size', 'command': ':MSIZ?', 'chars': 19,
             'minChars': 18, 'payloadLocation': (5, -2),
             'noChannelPrefix': True, 'SI': -2},
        ]

    def __init__(self, address, channel, cols):
        self.theTime = time.time()
        self.channel = channel[:2]
        self.cols = cols
        try:
            self.rm = pyvisa.ResourceManager()
            self.instr = self.rm.open_resource(address)
        except pyvisa.errors.VisaIOError:
            log.logger.warn(f'Failed to open resource: {address}.')
            raise(ScopeInitializationError)

    def __del__(self):
        log.logger.debug("Acquire destructor called")
        try:
            self.instr.close()
        except pyvisa.errors.VisaIOError:
            log.logger.warn('Exception occured while closing instrument')
            pass

    def update(self):
        """ Read the next trace from the oscillocope

        Read parameters as to the format and scale of the trace, read
        the raw data points, apply scale and offset information to
        the data

        Returns: *False* if there is an error.  Otherwise, return a
                 tuple of two equal size lists of float.  The first
                 element is a list of *float* representing time
                 values, and a list of *float* representing voltages. 
        """

        result = {}

        # Acquire the information for the trace based upon the
        # parameters defined in traceinfo.  This information will allow
        # us to convert the raw data into measured voltages, and allow
        # us to determine the timing information for each datum.

        for command in Acquire.traceinfo:

            try:
                message = None
                message = (self.instr.query(
                    command['command'] if 'noChannelPrefix' in command
                    else self.channel + command['command']))
                result[command['name']] = float(message[
                    command['payloadLocation'][0]:
                    command['payloadLocation'][1]]
                )
                if 'SI' in command:
                    multiplier = 1
                    log.logger.debug(f"SI length multiplier = {message[command['SI']]}")
                    if message[command['SI']] == 'M':
                        multiplier = 1e6
                    if message[command['SI']] == 'K':
                        multiplier = 1e3
                    result[command['name']] *= multiplier

            except (TypeError, ValueError):
                log.logger.warn(f"Error converting {command['name']}.")
                log.logger.warn(f'Message was {message}')
                log.logger.warn(
                    f"Expected Payload at {command['payloadLocation']}")
                return False

        # We have successfully read the trace parameters from the
        # scope.  Now, acquire the actual trace information.

        skip = int(result['size'] / self.cols)
        log.logger.debug(f"Scope memory size = {result['size']}. "
                         f"Skip factor : {skip}")
        self.instr.write(f'wfsu SP,{skip},NP,{self.cols}')
        log.logger.debug(
            f"Waveform setup response: {self.instr.query('wfsu?')}")
        result['payload'] = self.instr.query_binary_values(
            self.channel + ':wf? dat2',
            datatype='b')
        #data = list(filter(lambda x: x % skip == 0, data))
        if len(result['payload']) < self.cols:
            log.logger.warn(
                f"Trace length underrun :{len(result['payload'])} bytes")
            return None
        if len(result['payload']) > self.cols:
            log.logger.warn(
                f"Trace length overrun :{len(result['payload'])} bytes")
            return None
        

        # We have successfully read the raw trace information from the
        # scope.  Apply the scale factors to both axis.

        length = len(result['payload'])
        timebase = [i * (1/result['sampleRate']) * skip
                    for i in range(length)
                    if not i % int(length/self.cols)][:self.cols]
        return (timebase,
                list(map(lambda x: x * result['vdiv']/25 - result['offset'],
                         result['payload'])))


def main(cols, timeout, address, channel, pipe):
    """Stream traces from a Siglent oscilloscope to a pipe.

    Read traces from a Siglent 1204x-E oscilloscope and stream those
    traces to the main program through a pipe.  We also will receive
    commands through that pipe.  Handle those commands and respnd to
    those cmmands through the pipe as well.  Commands and responses to
    those commands will be of the type 'Message' from the class
    defined above.  The traces are sent as a 2-tuple of lists.  The
    first list represents the time values of the samples, while the
    second list represents the voltages at the time values.

    Args:
        cols (int):    The expected size of the lists to be sent through
                       the pipe.

        timeout (int): The maximum time this process is to run.  0
                       implys no timeout

        address (str): The *visa* address of the oscilloscope

        channel (str): The name of the oscilloscope channel to stream.

        pipe (pipe):   The pipe through which data are communicated to
                       and from the main program.

    Returns:
        None: *None*

    """

    threading.currentThread().name = "acquire"

    run = True
    startTime = time.time()

    def sigint_handler(*args):
        """sigint_Handler: Kill main loop if Ctrl-C is caught"""
        log.logger.debug("Caught Keyboard Interrupt. "
                         "exiting background process")
        run = False

    signal.signal(signal.SIGINT, sigint_handler)

    try:
        instrument = Acquire(address, channel, cols)
    except ScopeInitializationError:
        log.logger.info("Scope Initialization error,  Process exiting")
        return

    while run:
        if pipe.poll():
            message = pipe.recv()
            log.logger.info(f'Received message type {type(message)}')
            if type(message) == Message:
                log.logger.debug(f'was {message.command}')
                if message.command == 'halt':
                    run = False
                if message.command == 'ping':
                    pipe.send(Message('pong'))
        if (timeout > 0
           and time.time() - startTime > timeout):
            run = False
            log.logger.info('Background timeout')
            pipe.send(Message('Background timeout'))

        data = instrument.update()
        try:
            if data := instrument.update():
                pipe.send(data)
        except (pyvisa.errors.VisaIOError, pyvisa.errors.InvalidSession):
            run = False
            log.logger.warn("Fatal error communicating with the instrument")

log.logger.info("Process exiting")
