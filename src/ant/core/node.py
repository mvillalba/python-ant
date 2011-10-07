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
from ant.core.exceptions import *
from ant.core import message
from ant.core import event


class NetworkKey(object):
    def __init__(self, name=None, key='\x00' * 8):
        self.key = key
        if name:
            self.name = name
        else:
            self.name = str(uuid.uuid4())
        self.number = 0


class Channel(event.EventCallback):
    cb_lock = thread.allocate_lock()

    def __init__(self, node):
        self.node = node
        self.is_free = True
        self.name = str(uuid.uuid4())
        self.number = 0
        self.cb = []
        self.node.evm.registerCallback(self)

    def __del__(self):
        self.node.evm.removeCallback(self)

    def assign(self, net_key, ch_type):
        msg = message.ChannelAssignMessage(number=self.number)
        msg.setNetworkNumber(self.node.getNetworkKey(net_key).number)
        msg.setChannelType(ch_type)
        self.node.driver.write(msg.encode())
        if self.node.evm.waitForAck(msg) != RESPONSE_NO_ERROR:
            raise ChannelError('Could not assign channel.')
        self.is_free = False

    def setID(self, dev_type, dev_num, trans_type):
        msg = message.ChannelIDMessage(number=self.number)
        msg.setDeviceType(dev_type)
        msg.setDeviceNumber(dev_num)
        msg.setTransmissionType(trans_type)
        self.node.driver.write(msg.encode())
        if self.node.evm.waitForAck(msg) != RESPONSE_NO_ERROR:
            raise ChannelError('Could not set channel ID.')

    def setSearchTimeout(self, timeout):
        msg = message.ChannelSearchTimeoutMessage(number=self.number)
        msg.setTimeout(timeout)
        self.node.driver.write(msg.encode())
        if self.node.evm.waitForAck(msg) != RESPONSE_NO_ERROR:
            raise ChannelError('Could not set channel search timeout.')

    def setPeriod(self, counts):
        msg = message.ChannelPeriodMessage(number=self.number)
        msg.setChannelPeriod(counts)
        self.node.driver.write(msg.encode())
        if self.node.evm.waitForAck(msg) != RESPONSE_NO_ERROR:
            raise ChannelError('Could not set channel period.')

    def setFrequency(self, frequency):
        msg = message.ChannelFrequencyMessage(number=self.number)
        msg.setFrequency(frequency)
        self.node.driver.write(msg.encode())
        if self.node.evm.waitForAck(msg) != RESPONSE_NO_ERROR:
            raise ChannelError('Could not set channel frequency.')

    def open(self):
        msg = message.ChannelOpenMessage(number=self.number)
        self.node.driver.write(msg.encode())
        if self.node.evm.waitForAck(msg) != RESPONSE_NO_ERROR:
            raise ChannelError('Could not open channel.')

    def close(self):
        msg = message.ChannelCloseMessage(number=self.number)
        self.node.driver.write(msg.encode())
        if self.node.evm.waitForAck(msg) != RESPONSE_NO_ERROR:
            raise ChannelError('Could not close channel.')

        while True:
            msg = self.node.evm.waitForMessage(message.ChannelEventMessage)
            if msg.getMessageCode() == EVENT_CHANNEL_CLOSED:
                break

    def unassign(self):
        msg = message.ChannelUnassignMessage(number=self.number)
        self.node.driver.write(msg.encode())
        if self.node.evm.waitForAck(msg) != RESPONSE_NO_ERROR:
            raise ChannelError('Could not unassign channel.')
        self.is_free = True

    def registerCallback(self, callback):
        self.cb_lock.acquire()
        if callback not in self.cb:
            self.cb.append(callback)
        self.cb_lock.release()

    def process(self, msg):
        self.cb_lock.acquire()
        if isinstance(msg, message.ChannelMessage) and \
        msg.getChannelNumber() == self.number:
            for callback in self.cb:
                try:
                    callback.process(msg)
                except:
                    pass  # Who cares?
        self.cb_lock.release()


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
            self.channels.append(Channel(self))
            self.channels[i].number = i
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
        self.networks[number].number = number

    def getNetworkKey(self, name):
        for netkey in self.networks:
            if netkey.name == name:
                return netkey
        raise NodeError('Could not find network key with the supplied name.')

    def getFreeChannel(self):
        for channel in self.channels:
            if channel.is_free:
                return channel
        raise NodeError('Could not find free channel.')

    def registerEventListener(self, callback):
        self.evm.registerCallback(callback)

    def process(self, msg):
        pass
