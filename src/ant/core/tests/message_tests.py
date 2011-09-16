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

    def test_setPayload(self):
        self.assertRaises(MessageException, self.message.setPayload,
                          '\xFF' * 15)
        self.assertTrue(self.message.setPayload('\x11') is None)

    def test_setType(self):
        self.assertRaises(MessageException, self.message.setType, -1)
        self.assertRaises(MessageException, self.message.setType, 300)
        self.assertTrue(self.message.setType(0x23) is None)

    def test_getChecksum(self):
        self.message = Message(type=MESSAGE_SYSTEM_RESET, payload='\x00')
        self.assertEquals(self.message.getChecksum(), 0xEF)
        self.message = Message(type=MESSAGE_ASSIGN_CHANNEL,
                               payload='\x00' * 3)
        self.assertEquals(self.message.getChecksum(), 0xE5)

    def test_encode(self):
        self.message = Message(type=MESSAGE_ASSIGN_CHANNEL,
                               payload='\x00' * 3)
        self.assertEqual(self.message.encode(),
                         '\xA4\x03\x42\x00\x00\x00\xE5')

    def test_decode(self):
        self.assertRaises(MessageException, self.message.decode,
                          '\xA5\x03\x42\x00\x00\x00\xE5')
        self.assertEqual(self.message.decode('\xA4\x03\x42\x00\x00\x00\xE5'),
                         7)
        self.assertEqual(self.message.getType(), MESSAGE_ASSIGN_CHANNEL)
        self.assertEqual(self.message.getPayload(), '\x00' * 3)
        self.assertEqual(self.message.getChecksum(), 0xE5)

class SystemResetMessageTest(unittest.TestCase):
    def setUp(self):
        self.message = SystemResetMessage()

    def test_encode(self):
        self.assertEqual(self.message.encode(), '\xA4\x01\x4A\x00\xEF')
