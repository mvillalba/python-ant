"""
Initialize a basic broadcast slave channel for listening to
an ANT+ HR monitor.

"""

import sys
import time

from codinghyde.ant import driver
from codinghyde.ant import node
from codinghyde.ant.constants import *

from config import *

NETKEY = '\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'

# Initialize
stick = driver.USB1Driver(SERIAL, debug=DEBUG)
antnode = node.Node(stick)
antnode.start()

# Set network key
key = node.NetworkKey('ANT+', NETKEY)
antnode.setNetworkKey(key)

# Get the first unused channel. Returns an instance of the node.Channel class.
channel = antnode.getChannel()

# Let's give our channel a nickname
channel.setName('HRM')

# Initialize it as a receiving channel using our network key
channel.assign(key, CHANNEL_BROADCAST_RECEIVE)

# Now set the channel id for pairing with an ANT+ HR monitor
channel.setID(DEVICE_SEARCH, 120, TRANSFER_PAIRING)

# Listen forever and ever
channel.setSearchTimeout(TIMEOUT_NEVER)

# We want a ~4.06 Hz transmission period
channel.setPeriod(8070)

# And ANT frequency 57
channel.setFrequency(57)

# Time to go live
channel.open()

print "Listening for HR monitor events (120 seconds)..."
time.sleep(120)

# Shutdown channel
channel.close()
channel.unassign()

# Shutdown
antnode.stop()
