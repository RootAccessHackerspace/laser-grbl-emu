#!/usr/bin/python3

##############################################################################
# Implementation of a "fake" serial module that emulates GRBL
# Mimics pySerial
#
#
# Dylan Armitage
##############################################################################

__author__ = "Dylan Armitage"
__email__ = "d.armitage89@gmail.com"
__license__ = "MIT"

import logging
import coloredlogs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Serial:
    
    def __init__(self, port='/dev/ttyAMA0', baudrate=115200, timeout=1, bytesize=8,
                 parity='N', stopbits=1, xonxoff=0, rtscts=0):
        self.name = name
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self._open = True
        self._received_data = ''
        self._data = 'Grbl v1.1f [\'$\' for help]\n'
        logger.debug('fakeSerial initialized')

    def is_open(self):
        return self._open

    def open(self):
        self._open = True

    def close(self):
        self._open = False

    def read(self, n=1):
        # Read n characters from the output buffer
        try:
            buff = self._data[0:n]
            self._data = self._data[n:]
        except IndexError:
            logger.debug('No data in buffer')
            buff = ''
        return buff

    def readline(self):
        # Read individual characters until newline found
        try:
            newline = self._data.index('\n')
            if newline != -1:
                buff = self._data[0:newline+1]
                self._data = self._data[newline+1:]
            else:
                logger.debug('No data in buffer')
                buff = ''
        except IndexError:
            logger.debug('No data in buffer')
            buff = ''
        return buff

    def write(self, string):
        # TODO: Process the string written to append the appropriate response
        logger.info('fakeSerial received %s', string)
        self._received_data += string
