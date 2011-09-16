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

import struct

from ant.core.exceptions import MessageError
from ant.core.constants import *

class Message(object):
    def __init__(self, type=0x00, payload=''):
        self.setType(type)
        self.setPayload(payload)

    def getPayload(self):
        return self.payload

    def setPayload(self, payload):
        if len(payload) > 9:
            raise MessageError(
                  'Could not set payload (payload too long).')

        self.payload = payload

    def getType(self):
        return self.type

    def setType(self, type):
        if (type > 0xFF) or (type < 0x00):
            raise MessageError('Could not set type (type out of range).')

        self.type = type

    def getChecksum(self):
        data = chr(len(self.getPayload()))
        data += chr(self.getType())
        data += self.getPayload()

        checksum = MESSAGE_TX_SYNC
        for byte in data:
            checksum = (checksum ^ ord(byte)) % 0xFF

        return checksum

    def getSize(self):
        return len(self.getPayload()) + 4

    def encode(self):
        raw = struct.pack('BBB',
                          MESSAGE_TX_SYNC,
                          len(self.getPayload()),
                          self.getType())
        raw += self.getPayload()
        raw += chr(self.getChecksum())

        return raw

    def decode(self, raw):
        sync, length, type = struct.unpack('BBB', raw[:3])
        if sync != MESSAGE_TX_SYNC:
            raise MessageError('Could not decode (expected TX sync).')
        if length > 9:
            raise MessageError('Could not decode (payload too long).')

        self.setType(type)
        self.setPayload(raw[3:length + 3])

        if self.getChecksum() != ord(raw[length + 3]):
            raise MessageError('Could not decode (bad checksum).')

        return self.getSize()

class ChannelMessage(Message):
    def __init__(self, type, payload='', number=0x00):
        Message.__init__(type, '\x00' + payload)
        self.setChannelNumber(number)

    def getChannelNumber(self):
        return ord(self.getPayload()[0])

    def setChannelNumber(self, number):
        if (number > 0xFF) or (number < 0x00):
            raise MessageError('Could not set channel number ' \
                                   '(out of range).')

        self.payload[0] = chr(number)

class UnassignChannelMessage(ChannelMessage):
    def __init__(self, number=0x00):
        ChannelMessage.__init__(self, type=MESSAGE_CHANNEL_UNASSIGN,
                         number=number)

class AssignChannelMessage(ChannelMessage):
    def __init__(self, number=0x00, type=0x00, network=0x00):
        payload = struct.pack('BB', type, network)
        ChannelMessage.__init__(self, type=MESSAGE_CHANNEL_ASSIGN,
                                payload=payload, number=number)

    def getChannelType(self):
        return ord(self.getPayload()[1])

    def setChannelType(self, type):
        self.payload[1] = chr(type)

    def getNetworkNumber(self):
        return ord(self.getPayload()[2])

    def setNetworkNumber(self):
        self.payload[2] = chr(type)

class ChannelIDMessage(ChannelMessage):
    def __init__(self, number=0x00, device_number=0x00, device_type=0x00,
                 trans_type=0x00):
        payload = struct.pack('<HBB', device_number, device_type, trans_type)
        ChannelMessage.__init__(self, type=MESSAGE_CHANNEL_ID,
                                payload=payload, number=number)

    def getDeviceNumber(self):
        return struct.unpack('<H', self.payload[1:3])

    def setDeviceNumber(self, device_number):
        data = struct.pack('<H', device_number)
        self.payload[1] = data[1]
        self.payload[2] = data[2]

    def getDeviceType(self):
        return ord(self.payload[3])

    def setDeviceType(self, device_type):
        self.payload[3] = chr(device_type)

    def getTransmissionType(self):
        return ord(self.payload[4])

    def setTransmissionType(self, trans_type):
        self.payload[4] = chr(trans_type)

class ChanelPeriodMessage(ChannelMessage):
    def __init__(self, number=0x00, period=8192):
        payload = struct.pack('<H', period)
        ChannelMessage.__init__(self, type=MESSAGE_CHANNEL_PERIOD,
                                payload=payload, number=number)

    def getChannelPeriod(self):
        return struct.unpack('<H', self.payload[1:3])

    def setChannelPeriod(self, period):
        data = struct.pack('<H', period)
        self.payload[1] = data[1]
        self.payload[2] = data[2]

def ChannelSearchTimeoutMessage(ChannelMessage):
    def __init__(self, number=0x00, timeout=0xFF):
        ChannelMessage.__init__(self, type=MESSAGE_CHANNEL_SEARCH_TIMEOUT,
                                payload=chr(timeout), number=number)

    def getTimeout(self):
        return ord(self.payload[1])

    def setTimeout(self, timeout):
        self.payload[1] = chr(timeout)

def ChannelFrequencyMessage(ChannelMessage):
    def __init__(self, number=0x00, frequency=66):
        ChannelMessage.__init__(self, type=MESSAGE_CHANNEL_FREQUENCY,
                                payload=chr(frequency), number=number)

    def getFrequency(self):
        return ord(self.payload[1])

    def setFrequency(self, frequency):
        self.payload[1] = chr(frequency)

def ChannelTXPowerMessage(ChannelMessage):
    def __init__(self, number=0x00, power=0x00):
        ChannelMessage.__init__(self, type=MESSAGE_CHANNEL_TX_POWER,
                                payload=chr(power), number=number)

    def getPower(self):
        return ord(self.payload[1])

    def setPower(self, power):
        self.payload[1] = chr(power)

def NetworkKeyMessage(Message):
    def __init__(self, number=0x00, key='\x00' * 8):
        payload = chr(number) + key
        Message__init__(self, type=MESSAGE_NETWORK_KEY, payload=payload)

    def getNumber(self):
        return ord(self.payload[0])

    def setNumber(self, number):
        self.payload[0] = chr(number)

    def getKey(self):
        return self.payload[1:]

    def setKey(self, key):
        self.payload = self.payload[0] + key

def TXPowerMessage(Message):
    def __init__(self, power=0x00):
        payload = struct.pack('BB', 0x00, power)
        Message.__init__(self, type=MESSAGE_TX_POWER, payload=payload)

    def getPower(self):
        return ord(self.payload[1])

    def setPower(self, power):
        self.payload[1] = chr(power)

class SystemResetMessage(Message):
    def __init__(self):
        Message.__init__(self, type=MESSAGE_SYSTEM_RESET, payload='\x00')


