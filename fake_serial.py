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
from pygcode import Machine, Line

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#### GRBL responses ##########################################################
OK = 'ok'
SETTING_DISABLED = 'error:Setting disabled'
NOT_IDLE = 'error:Not idle'
ALARM_LOCK = 'error:Alarm lock'
LINE_OVERFLOW = 'error:Line overflow'
MODAL_VIOLATION = 'error:Modal group violation'
UNSUPPORTED_COMMAND = 'error:Unsupported command'
UNDEFINED_FEED = 'error:Undefined feed rate'
INVALID_GCODE = {'not integer': 'error:Invalid gcode ID:23',
                 'both xyz': 'error:Invalid gcode ID:24',
                 'repeated': 'error:Invalid gcode ID:25',
                 'no xyz': 'error:Invalid gcode ID:26',
                 'nline oor': 'error:Invalid gcode ID:27',
                 'missing pl': 'error:Invalid gcode ID:28',
                 'unsup wcs': 'error:Invalid gcode ID:29',
                 'wrong g53 mode': 'error:Invalid gcode ID:30',
                 'unused axis': 'error:Invalid gcode ID:31',
                 'no xyz arc': 'error:Invalid gcode ID:32',
                 'invalid target': 'error:Invalid gcode ID:33',
                 'arc geom rad': 'error:Invalid gcode ID:34',
                 'arc miss IJK': 'error:Invalid gcode ID:35',
                 'unused words': 'error:Invalid gcode ID:36',
                 'tool offset axis': 'error:Invalid gcode ID:37'
                }
ALARM_HLIM = 'ALARM:Hard limit'
ALARM_SLIM = 'ALARM:Soft limit'
ALARM_ABORT = 'ALARM:Abort during cycle'
RESET_CONTINUE = '[reset to continue]'
TO_UNLOCK = '[\'$H\'|\'$X\' to unlock]'
CAUTION = '[Caution: Unlocked]'
ENABLED = '[Enabled]'
DISABLED = '[Disabled]'
IDLE = 'Idle'
RUNNING = 'Run'
ALARM = 'ALARM'

class grbl_interpret:
    '''A simple python implementation of grbl

    Mostly just makes sure valid gcode is being used
    '''
    def __init__(self):
        self.state_pos = {'state': IDLE,
                          'mpos': [0.000, 0.000, 0.000],
                          'wpos': [0.000, 0.000, 0.000],
                          'plan buf': 0,
                          'rx buf': 0
                         }
        self.mach = Machine()

    def input(self, line):
        pass


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
