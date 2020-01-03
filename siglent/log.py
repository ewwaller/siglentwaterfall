# MIT License
#
# Copyright (c) 2018 Eric Waller
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


import logging


def setLog(LogLevelStr):
    """
    Set the log level to be used during this run.
    This program uses logging to provide warning, info, and debug
    level messages. Wwarnings are always enabled.  info level messages
    are considered to be "Verbose".

    Args:
       LogLevelStr: A string representing on of the members of logging that
                    define log levels ("CRITICAL", DEBUG", "ERROR", "FATAL"
                    ("INFO", "NOTSET", WARN, "WARNING")
    """
    logger.setLevel(getattr(logging, LogLevelStr))
    logger.info("Log configuration set to %s", LogLevelStr)


logFormat = '%(asctime)s %(name)s (%(threadName)s) %(levelname)s : %(message)s'
logger = logging.getLogger('main')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(logFormat))
logger.addHandler(handler)
setLog('WARN')

def setLogFile(path):
    handler = logging.FileHandler(path)
    handler.setFormatter(logging.Formatter(logFormat))
    logger.addHandler(handler)
    logger.info(f"Set log file to {path}")
