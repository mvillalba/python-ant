"""
Extending on demo 05, request stick capabilities using raw messages.

"""

import sys
import time

from ant.core import driver
from ant.core import message
from ant.core.constants import *

from config import *

# Initialize
stick = driver.USB1Driver(SERIAL, log=LOG, debug=DEBUG)
stick.open()

# Reset stick
msg = message.SystemResetMessage()
stick.write(msg.encode())
time.sleep(1)

# Request stick capabilities
msg = message.ChannelRequestMessage()
msg.setMessageID(MESSAGE_CAPABILITIES)
stick.write(msg.encode())

# Read response
hdlfinder = message.Message()
capmsg = hdlfinder.getHandler(stick.read(8))

print 'Std Options:', capmsg.getStdOptions()
print 'Adv Options:', capmsg.getAdvOptions()
print 'Adv Options 2:', capmsg.getAdvOptions2()
print 'Max Channels:', capmsg.getMaxChannels()
print 'Max Networks:', capmsg.getMaxNetworks()

# Shutdown
stick.close()
