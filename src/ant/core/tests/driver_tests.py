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

from ant.core.driver import *


class DummyDriver(Driver):
    def _open(self):
        pass

    def _close(self):
        pass

    def _read(self, count):
        return '\x00' * count

    def _write(self, data):
        return len(data)


class DriverTest(unittest.TestCase):
    def setUp(self):
        self.driver = DummyDriver('superdrive')

    def tearDown(self):
        pass

    def test_isOpen(self):
        self.assertFalse(self.driver.isOpen())
        self.driver.open()
        self.assertTrue(self.driver.isOpen())
        self.driver.close()
        self.assertFalse(self.driver.isOpen())

    def test_open(self):
        self.driver.open()
        self.assertRaises(DriverError, self.driver.open)
        self.driver.close()

    def test_close(self):
        pass    # Nothing to test for

    def test_read(self):
        self.assertFalse(self.driver.isOpen())
        self.assertRaises(DriverError, self.driver.read, 1)
        self.driver.open()
        self.assertEqual(len(self.driver.read(5)), 5)
        self.assertRaises(DriverError, self.driver.read, -1)
        self.assertRaises(DriverError, self.driver.read, 0)
        self.driver.close()

    def test_write(self):
        self.assertRaises(DriverError, self.driver.write, '\xFF')
        self.driver.open()
        self.assertRaises(DriverError, self.driver.write, '')
        self.assertEquals(self.driver.write('\xFF' * 10), 10)
        self.driver.close()


# How do you even test this without hardware?
class USB1DriverTest(unittest.TestCase):
    def _open(self):
        pass

    def _close(self):
        pass

    def _read(self):
        pass

    def _write(self):
        pass
