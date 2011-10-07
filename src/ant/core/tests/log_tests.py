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

LOG_LOCATION = '/tmp/python-ant.logtest.ant'

import unittest

from ant.core.log import *


class LogReaderTest(unittest.TestCase):
    def setUp(self):
        lw = LogWriter(LOG_LOCATION)
        lw.logOpen()
        lw.logRead('\x01')
        lw.logWrite('\x00')
        lw.logRead('TEST')
        lw.logClose()
        lw.close()

        self.log = LogReader(LOG_LOCATION)

    def test_open_close(self):
        self.assertTrue(self.log.is_open)
        self.log.close()
        self.assertFalse(self.log.is_open)
        self.log.open(LOG_LOCATION)
        self.assertTrue(self.log.is_open)

    def test_read(self):
        t1 = self.log.read()
        t2 = self.log.read()
        t3 = self.log.read()
        t4 = self.log.read()
        t5 = self.log.read()

        self.assertEquals(self.log.read(), None)

        self.assertEquals(t1[0], EVENT_OPEN)
        self.assertTrue(isinstance(t1[1], int))
        self.assertEquals(len(t1), 2)

        self.assertEquals(t2[0], EVENT_READ)
        self.assertTrue(isinstance(t1[1], int))
        self.assertEquals(len(t2), 3)
        self.assertEquals(t2[2], '\x01')

        self.assertEquals(t3[0], EVENT_WRITE)
        self.assertTrue(isinstance(t1[1], int))
        self.assertEquals(len(t3), 3)
        self.assertEquals(t3[2], '\x00')

        self.assertEquals(t4[0], EVENT_READ)
        self.assertEquals(t4[2], 'TEST')

        self.assertEquals(t5[0], EVENT_CLOSE)
        self.assertTrue(isinstance(t1[1], int))
        self.assertEquals(len(t5), 2)


class LogWriterTest(unittest.TestCase):
    def setUp(self):
        self.log = LogWriter(LOG_LOCATION)

    def test_open_close(self):
        self.assertTrue(self.log.is_open)
        self.log.close()
        self.assertFalse(self.log.is_open)
        self.log.open(LOG_LOCATION)
        self.assertTrue(self.log.is_open)

    def test_log(self):
        # Redundant, any error in log* methods will cause the LogReader test
        # suite to fail.
        pass
