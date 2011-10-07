"""
Interrogate stick for supported capabilities.

"""

import sys

from ant.core import driver
from ant.core import node

from config import *

# Initialize
stick = driver.USB1Driver(SERIAL, log=LOG, debug=DEBUG)
antnode = node.Node(stick)
antnode.start()

# Interrogate stick
# Note: This method will return immediately, as the stick's capabilities are
# interrogated on node initialization (node.start()) in order to set proper
# internal Node instance state.
capabilities = antnode.getCapabilities()

print 'Maximum channels:', capabilities[0]
print 'Maximum network keys:', capabilities[1]
print 'Standard options: %X' % capabilities[2][0]
print 'Advanced options: %X' % capabilities[2][1]

# Shutdown
antnode.stop()
