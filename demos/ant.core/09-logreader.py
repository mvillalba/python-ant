"""
Read an ANT-LOG file.

"""

import sys

from ant.core import log

from config import *

# Open log
if len(sys.argv) != 2:
    print "Usage: {0} file.ant".format(sys.argv[0])
    sys.exit()

lr = log.LogReader(sys.argv[1])

event = lr.read()
while (event != None):
    if event[0] == log.EVENT_OPEN:
        title = 'EVENT_OPEN'
    elif event[0] == log.EVENT_CLOSE:
        title = 'EVENT_CLOSE'
    elif event[0] == log.EVENT_READ:
        title = 'EVENT_READ'
    elif event[0] == log.EVENT_WRITE:
        title = 'EVENT_WRITE'

    print '========== [{0}:{1}] =========='.format(title, event[1])
    if event[0] == log.EVENT_READ or event[0] == log.EVENT_WRITE:
        length = 8
        line = 0
        data = event[2]
        while data:
            row = data[:length]
            data = data[length:]
            hex_data = ['%02X' % ord(byte) for byte in row]
            print '%04X' % line, ' '.join(hex_data)

    print ''
    event = lr.read()
