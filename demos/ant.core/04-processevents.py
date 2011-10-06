"""
Extending on demo-03, implements an event callback we can use to process the
incoming data.

"""

import sys
import time

from ant.core import driver
from ant.core import node
from ant.core import event
from ant.core import message
from ant.core.constants import *

from config import *

NETKEY = '\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'

# A run-the-mill event listener
class HRMListener(event.EventCallback):
    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            print 'Heart Rate:', ord(msg.payload[-1])

# Initialize
stick = driver.USB1Driver(SERIAL, log=LOG, debug=DEBUG)
antnode = node.Node(stick)
antnode.start()

# Setup channel
key = node.NetworkKey('ANT+', NETKEY)
antnode.setNetworkKey(0, key)
channel = antnode.getFreeChannel()
channel.setName('HRM')
channel.assign(key, CHANNEL_BROADCAST_RECEIVE)
channel.setID(DEVICE_SEARCH, 120, TRANSFER_PAIRING)
channel.setSearchTimeout(TIMEOUT_NEVER)
channel.setPeriod(8070)
channel.setFrequency(57)
channel.open()

# Setup callback
# Note: We could also register an event listener for non-channel events by
# calling registerEventListener() on antnode rather than channel.
channel.registerCallback(callback)

# Wait
print "Listening for HR monitor events (120 seconds)..."
time.sleep(120)

# Shutdown
channel.close()
channel.unassign()
antnode.stop()
