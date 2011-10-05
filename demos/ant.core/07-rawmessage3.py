"""
Initialize a basic broadcast slave channel for listening to
an ANT+ Bicycle cadence and speed senser, using raw messages
and event handlers.

"""

import sys
import time

from ant.core import driver
from ant.core import event
from ant.core.constants import *
from ant.core.message import *

from config import *

NETKEY = '\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'

# Event callback
class MyCallback(event.EventCallback):
    def process(self, msg):
        print msg

# Initialize driver
stick = driver.USB1Driver(SERIAL, log=LOG, debug=DEBUG)
stick.open()

# Initialize event machine
evm = event.EventMachine(stick)
evm.registerCallback(MyCallback())
evm.start()

# Reset
msg = SystemResetMessage()
stick.write(msg.encode())
time.sleep(1)

# Set network key
msg = NetworkKeyMessage(key=NETKEY)
stick.write(msg.encode())
if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
    sys.exit()

# Initialize it as a receiving channel using our network key
msg = ChannelAssignMessage()
stick.write(msg.encode())
if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
    sys.exit()

# Now set the channel id for pairing with an ANT+ bike cadence/speed sensor
msg = ChannelIDMessage(device_type=121)
stick.write(msg.encode())
if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
    sys.exit()

# Listen forever and ever (not really, but for a long time)
msg = ChannelSearchTimeoutMessage(timeout=255)
stick.write(msg.encode())
if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
    sys.exit()

# We want a ~4.05 Hz transmission period
msg = ChannelPeriodMessage(period=8085)
stick.write(msg.encode())
if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
    sys.exit()

# And ANT frequency 57, of course
msg = ChannelFrequencyMessage(frequency=57)
stick.write(msg.encode())
if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
    sys.exit()

# Time to go live
msg = ChannelOpenMessage()
stick.write(msg.encode())
if evm.waitForAck(msg) != RESPONSE_NO_ERROR:
    sys.exit()

print "Listening for ANT events (120 seconds)..."
time.sleep(120)

# Shutdown
msg = SystemResetMessage()
stick.write(msg.encode())
time.sleep(1)

evm.stop()
stick.close()
