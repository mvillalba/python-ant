"""
Interrogate stick for supported capabilities.

"""

import sys

from codinghyde.ant import driver
from codinghyde.ant import node

from config import *

# Initialize
stick = driver.USB1Driver(SERIAL, debug=DEBUG)
antnode = node.Node(stick)
antnode.start()

# Interrogate stick
# Note: This method will return immediately, as the stick's capabilities are
# interrogated on node initialization (node.start()) in order to set proper
# internal Node instance state.
capabilities = antnode.getCapabilities()

print 'Maximum channels:', capabilities['max_channels']
print 'Maximum network keys:', capabilities['max_net_keys']
print 'Standard options: %X' % capabilities['std_options']
print 'Advanced options: %X' % capabilities['adv_options']

# Shutdown
antnode.stop()
