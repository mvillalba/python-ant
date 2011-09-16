"""
Extending on demo-03, implements an event callback we can use to process the
incoming data.

"""

import sys
import time

from codinghyde.ant import driver
from codinghyde.ant import node
from codinghyde.ant import event
from codinghyde.ant.constants import *

from config import *

NETKEY = '\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'

# A run-the-mill event listener
class HRMListener(event.ChannelEventListener):
    # We are only interested in the payloads arriving through our channel
    def receiveBroadcast(event):
        print 'Heart Rate:', ord(event.payload[-1])

# Initialize
stick = driver.USB1Driver(SERIAL, debug=DEBUG)
antnode = node.Node(stick)
antnode.start()

# Setup channel
key = node.NetworkKey('ANT+', NETKEY)
antnode.setNetworkKey(key)
channel = antnode.getChannel()
channel.setName('HRM')
channel.assign(key, CHANNEL_BROADCAST_RECEIVE)
channel.setID(DEVICE_SEARCH, 120, TRANSFER_PAIRING)
channel.setSearchTimeout(TIMEOUT_NEVER)
channel.setPeriod(8070)
channel.setFrequency(57)
channel.open()

# Setup callback
# Note: We could also register an event listener for non-channel events by
# calling registerEventListener() on our node.
channel.registerEventListener(listener)

# Wait
print "Listening for HR monitor events (120 seconds)..."
time.sleep(120)

# Shutdown
channel.close()
channel.unassign()
antnode.stop()
