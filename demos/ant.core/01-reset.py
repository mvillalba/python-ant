"""
Perform basic node initialization and shutdown cleanly.

"""

import sys

from ant.core import driver
from ant.core import node

from config import *

# Initialize and configure our ANT stick's driver
stick = driver.USB1Driver(SERIAL, log=LOG, debug=DEBUG)

# Now create an ANT node, and pass it our driver so it can talk to the stick
antnode = node.Node(stick)

# Open driver if closed, start event listener, reset internal settings, and
# send a system reset command to the ANT stick (blocks).
try:
    antnode.start()
except driver.DriverError, e:
    print e
    sys.exit()

# At any point in our node's life, we could manually call reset() to re-
# initialize the stick and Node. Like this:
#antnode.reset()

# Stop the ANT node. This should close all open channels, and do final system
# reset on the stick. However, considering we just did a reset, we explicitly
# tell our node to skip the reset. This call will also automatically release
# the stick by calling close() on the driver.
antnode.stop(reset=False)
