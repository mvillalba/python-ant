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

import unittest

from ant.core.message import *


class MessageTest(unittest.TestCase):
    def setUp(self):
        self.message = Message()

    def test_get_setPayload(self):
        self.assertRaises(MessageError, self.message.setPayload,
                          '\xFF' * 15)
        self.message.setPayload('\x11' * 5)
        self.assertEquals(self.message.getPayload(), '\x11' * 5)

    def test_get_setType(self):
        self.assertRaises(MessageError, self.message.setType, -1)
        self.assertRaises(MessageError, self.message.setType, 300)
        self.message.setType(0x23)
        self.assertEquals(self.message.getType(), 0x23)

    def test_getChecksum(self):
        self.message = Message(type_=MESSAGE_SYSTEM_RESET, payload='\x00')
        self.assertEquals(self.message.getChecksum(), 0xEF)
        self.message = Message(type_=MESSAGE_CHANNEL_ASSIGN,
                               payload='\x00' * 3)
        self.assertEquals(self.message.getChecksum(), 0xE5)

    def test_getSize(self):
        self.message.setPayload('\x11' * 7)
        self.assertEquals(self.message.getSize(), 11)

    def test_encode(self):
        self.message = Message(type_=MESSAGE_CHANNEL_ASSIGN,
                               payload='\x00' * 3)
        self.assertEqual(self.message.encode(),
                         '\xA4\x03\x42\x00\x00\x00\xE5')

    def test_decode(self):
        self.assertRaises(MessageError, self.message.decode,
                          '\xA5\x03\x42\x00\x00\x00\xE5')
        self.assertRaises(MessageError, self.message.decode,
                          '\xA4\x14\x42' + ('\x00' * 20) + '\xE5')
        self.assertRaises(MessageError, self.message.decode,
                          '\xA4\x03\x42\x01\x02\xF3\xE5')
        self.assertEqual(self.message.decode('\xA4\x03\x42\x00\x00\x00\xE5'),
                         7)
        self.assertEqual(self.message.getType(), MESSAGE_CHANNEL_ASSIGN)
        self.assertEqual(self.message.getPayload(), '\x00' * 3)
        self.assertEqual(self.message.getChecksum(), 0xE5)

    def test_getHandler(self):
        handler = self.message.getHandler('\xA4\x03\x42\x00\x00\x00\xE5')
        self.assertTrue(isinstance(handler, ChannelAssignMessage))
        self.assertRaises(MessageError, self.message.getHandler,
                          '\xA4\x03\xFF\x00\x00\x00\xE5')
        self.assertRaises(MessageError, self.message.getHandler,
                          '\xA4\x03\x42')
        self.assertRaises(MessageError, self.message.getHandler,
                          '\xA4\x05\x42\x00\x00\x00\x00')


class ChannelMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = ChannelMessage(type_=MESSAGE_SYSTEM_RESET)

    def test_get_setChannelNumber(self):
        self.assertEquals(self.message.getChannelNumber(), 0)
        self.message.setChannelNumber(3)
        self.assertEquals(self.message.getChannelNumber(), 3)


class ChannelUnassignMessageTest(unittest.TestCase):
    # No currently defined methods need testing
    pass


class ChannelAssignMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = ChannelAssignMessage()

    def test_get_setChannelType(self):
        self.message.setChannelType(0x10)
        self.assertEquals(self.message.getChannelType(), 0x10)

    def test_get_setNetworkNumber(self):
        self.message.setNetworkNumber(0x11)
        self.assertEquals(self.message.getNetworkNumber(), 0x11)

    def test_payload(self):
        self.message.setChannelNumber(0x01)
        self.message.setChannelType(0x02)
        self.message.setNetworkNumber(0x03)
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03')


class ChannelIDMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = ChannelIDMessage()

    def test_get_setDeviceNumber(self):
        self.message.setDeviceNumber(0x10FA)
        self.assertEquals(self.message.getDeviceNumber(), 0x10FA)

    def test_get_setDeviceType(self):
        self.message.setDeviceType(0x10)
        self.assertEquals(self.message.getDeviceType(), 0x10)

    def test_get_setTransmissionType(self):
        self.message.setTransmissionType(0x11)
        self.assertEquals(self.message.getTransmissionType(), 0x11)

    def test_payload(self):
        self.message.setChannelNumber(0x01)
        self.message.setDeviceNumber(0x0302)
        self.message.setDeviceType(0x04)
        self.message.setTransmissionType(0x05)
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03\x04\x05')


class ChannelPeriodMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = ChannelPeriodMessage()

    def test_get_setChannelPeriod(self):
        self.message.setChannelPeriod(0x10FA)
        self.assertEquals(self.message.getChannelPeriod(), 0x10FA)

    def test_payload(self):
        self.message.setChannelNumber(0x01)
        self.message.setChannelPeriod(0x0302)
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03')


class ChannelSearchTimeoutMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = ChannelSearchTimeoutMessage()

    def test_get_setTimeout(self):
        self.message.setTimeout(0x10)
        self.assertEquals(self.message.getTimeout(), 0x10)

    def test_payload(self):
        self.message.setChannelNumber(0x01)
        self.message.setTimeout(0x02)
        self.assertEquals(self.message.getPayload(), '\x01\x02')


class ChannelFrequencyMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = ChannelFrequencyMessage()

    def test_get_setFrequency(self):
        self.message.setFrequency(22)
        self.assertEquals(self.message.getFrequency(), 22)

    def test_payload(self):
        self.message.setChannelNumber(0x01)
        self.message.setFrequency(0x02)
        self.assertEquals(self.message.getPayload(), '\x01\x02')


class ChannelTXPowerMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = ChannelTXPowerMessage()

    def test_get_setPower(self):
        self.message.setPower(0xFA)
        self.assertEquals(self.message.getPower(), 0xFA)

    def test_payload(self):
        self.message.setChannelNumber(0x01)
        self.message.setPower(0x02)
        self.assertEquals(self.message.getPayload(), '\x01\x02')


class NetworkKeyMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = NetworkKeyMessage()

    def test_get_setNumber(self):
        self.message.setNumber(0xFA)
        self.assertEquals(self.message.getNumber(), 0xFA)

    def test_get_setKey(self):
        self.message.setKey('\xFD' * 8)
        self.assertEquals(self.message.getKey(), '\xFD' * 8)

    def test_payload(self):
        self.message.setNumber(0x01)
        self.message.setKey('\x02\x03\x04\x05\x06\x07\x08\x09')
        self.assertEquals(self.message.getPayload(),
                          '\x01\x02\x03\x04\x05\x06\x07\x08\x09')


class TXPowerMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = TXPowerMessage()

    def test_get_setPower(self):
        self.message.setPower(0xFA)
        self.assertEquals(self.message.getPower(), 0xFA)

    def test_payload(self):
        self.message.setPower(0x01)
        self.assertEquals(self.message.getPayload(), '\x00\x01')


class SystemResetMessageTest(unittest.TestCase):
    # No currently defined methods need testing
    pass


class ChannelOpenMessageTest(unittest.TestCase):
    # No currently defined methods need testing
    pass


class ChannelCloseMessageTest(unittest.TestCase):
    # No currently defined methods need testing
    pass


class ChannelRequestMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = ChannelRequestMessage()

    def test_get_setMessageID(self):
        self.message.setMessageID(0xFA)
        self.assertEquals(self.message.getMessageID(), 0xFA)
        self.assertRaises(MessageError, self.message.setMessageID, 0xFFFF)

    def test_payload(self):
        self.message.setChannelNumber(0x01)
        self.message.setMessageID(0x02)
        self.assertEquals(self.message.getPayload(), '\x01\x02')


class ChannelBroadcastDataMessageTest(unittest.TestCase):
    # No currently defined methods need testing
    pass


class ChannelAcknowledgedDataMessageTest(unittest.TestCase):
    # No currently defined methods need testing
    pass


class ChannelBurstDataMessageTest(unittest.TestCase):
    # No currently defined methods need testing
    pass


class ChannelEventMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = ChannelEventMessage()

    def test_get_setMessageID(self):
        self.message.setMessageID(0xFA)
        self.assertEquals(self.message.getMessageID(), 0xFA)
        self.assertRaises(MessageError, self.message.setMessageID, 0xFFFF)

    def test_get_setMessageCode(self):
        self.message.setMessageCode(0xFA)
        self.assertEquals(self.message.getMessageCode(), 0xFA)
        self.assertRaises(MessageError, self.message.setMessageCode, 0xFFFF)

    def test_payload(self):
        self.message.setChannelNumber(0x01)
        self.message.setMessageID(0x02)
        self.message.setMessageCode(0x03)
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03')


class ChannelStatusMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = ChannelStatusMessage()

    def test_get_setStatus(self):
        self.message.setStatus(0xFA)
        self.assertEquals(self.message.getStatus(), 0xFA)
        self.assertRaises(MessageError, self.message.setStatus, 0xFFFF)

    def test_payload(self):
        self.message.setChannelNumber(0x01)
        self.message.setStatus(0x02)
        self.assertEquals(self.message.getPayload(), '\x01\x02')


class VersionMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = VersionMessage()

    def test_get_setVersion(self):
        self.message.setVersion('\xAB' * 9)
        self.assertEquals(self.message.getVersion(), '\xAB' * 9)
        self.assertRaises(MessageError, self.message.setVersion, '1234')

    def test_payload(self):
        self.message.setVersion('\x01' * 9)
        self.assertEquals(self.message.getPayload(), '\x01' * 9)


class CapabilitiesMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = CapabilitiesMessage()

    def test_get_setMaxChannels(self):
        self.message.setMaxChannels(0xFA)
        self.assertEquals(self.message.getMaxChannels(), 0xFA)
        self.assertRaises(MessageError, self.message.setMaxChannels, 0xFFFF)

    def test_get_setMaxNetworks(self):
        self.message.setMaxNetworks(0xFA)
        self.assertEquals(self.message.getMaxNetworks(), 0xFA)
        self.assertRaises(MessageError, self.message.setMaxNetworks, 0xFFFF)

    def test_get_setStdOptions(self):
        self.message.setStdOptions(0xFA)
        self.assertEquals(self.message.getStdOptions(), 0xFA)
        self.assertRaises(MessageError, self.message.setStdOptions, 0xFFFF)

    def test_get_setAdvOptions(self):
        self.message.setAdvOptions(0xFA)
        self.assertEquals(self.message.getAdvOptions(), 0xFA)
        self.assertRaises(MessageError, self.message.setAdvOptions, 0xFFFF)

    def test_get_setAdvOptions2(self):
        self.message.setAdvOptions2(0xFA)
        self.assertEquals(self.message.getAdvOptions2(), 0xFA)
        self.assertRaises(MessageError, self.message.setAdvOptions2, 0xFFFF)
        self.message = CapabilitiesMessage(adv_opts2=None)
        self.assertEquals(len(self.message.payload), 4)

    def test_payload(self):
        self.message.setMaxChannels(0x01)
        self.message.setMaxNetworks(0x02)
        self.message.setStdOptions(0x03)
        self.message.setAdvOptions(0x04)
        self.message.setAdvOptions2(0x05)
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03\x04\x05')


class SerialNumberMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = SerialNumberMessage()

    def test_get_setSerialNumber(self):
        self.message.setSerialNumber('\xFA\xFB\xFC\xFD')
        self.assertEquals(self.message.getSerialNumber(), '\xFA\xFB\xFC\xFD')
        self.assertRaises(MessageError, self.message.setSerialNumber,
                          '\xFF' * 8)

    def test_payload(self):
        self.message.setSerialNumber('\x01\x02\x03\x04')
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03\x04')
