# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2011, Martín Raúl Villalba
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
##############################################################################

import time
import thread
import uuid

from ant.core.constants import *
from ant.core import message
from ant.core import event

class NetworkKey(object):
    def __init__(self, name=None, key='\x00' * 8):
        self.key = key
        if name:
            self.name = name
        else:
            self.name = str(uuid.uuid4())
        
class Channel(event.EventCallback):
    def setName(self):
        pass

    def assign(self):
        pass

    def setID(self):
        pass

    def setSearchTimeout(self):
        pass

    def setPeriod(self):
        pass

    def setFrequency(self):
        pass

    def open(self):
        pass

    def close(self):
        pass

    def unassign(self):
        pass

    def registerEventListener(self, callback):
        pass

    def process(self, msg):
        pass

class Node(event.EventCallback):
    node_lock = thread.allocate_lock()

    def __init__(self, driver):
        self.driver = driver
        self.evm = event.EventMachine(self.driver)
        self.evm.registerCallback(self)
        self.networks = []
        self.channels = []
        self.running = False
        self.options = [0x00, 0x00, 0x00]

    def start(self):
        if self.running:
            raise NodeError('Could not start ANT node (already started).')

        if not self.driver.isOpen():
            self.driver.open()

        self.reset()
        self.evm.start()
        self.running = True
        self.init()

    def stop(self, reset=True):
        if not self.running:
            raise NodeError('Could not stop ANT node (not started).')

        if reset:
            self.reset()
        self.evm.stop()
        self.running = False
        self.driver.close()

    def reset(self):
        msg = message.SystemResetMessage()
        self.driver.write(msg.encode())
        time.sleep(1)

    def init(self):
        if not self.running:
            raise NodeError('Could not reset ANT node (not started).')

        msg = message.ChannelRequestMessage()
        msg.setMessageID(MESSAGE_CAPABILITIES)
        self.driver.write(msg.encode())

        caps = self.evm.waitForMessage(message.CapabilitiesMessage)

        self.networks = []
        for i in range(0, caps.getMaxNetworks()):
            self.networks.append(NetworkKey())
            self.setNetworkKey(i)
        self.channels = []
        for i in range(0, caps.getMaxChannels()):
            self.channels.append(Channel())
        self.options = (caps.getStdOptions(),
                        caps.getAdvOptions(),
                        caps.getAdvOptions2(),)

    def getCapabilities(self):
        return (len(self.channels),
                len(self.networks),
                self.options,)

    def setNetworkKey(self, number, key=None):
        if key:
            self.networks[number] = key

        msg = message.NetworkKeyMessage()
        msg.setNumber(number)
        msg.setKey(self.networks[number].key)
        self.driver.write(msg.encode())
        self.evm.waitForAck(msg)

    def getFreeChannel(self):
        pass

    def registerEventListener(self, callback):
        pass

    def process(self, msg):
        pass
