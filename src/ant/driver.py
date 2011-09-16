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

import serial

from codinghyde.ant.exceptions import DriverException

class Driver(object):
    def __init__(self, device, debug=False):
        self.device = device
        self.debug = debug
        self.is_open = False

    def isOpen(self):
        return self.is_open

    def open(self):
        if self.isOpen():
            raise DriverException("Could not open device (already open).")

        self._open()
        self.is_open = True

    def close(self):
        if not self.isOpen():
            raise DriverException("Could not close device (not open).")

        self._close()
        self.is_open = False

    def read(self, count):
        if not self.isOpen():
            raise DriverException("Could not read from device (not open).")
        if count <= 0:
            raise DriverException("Could not read from device (zero request).")

        data = self._read(count)

        if self.debug:
            self._dump(data, 'READ')

        return data

    def write(self, data):
        if not self.isOpen():
            raise DriverException("Could not write to device (not open).")
        if len(data) <= 0:
            raise DriverException("Could not write to device (no data).")

        if self.debug:
            self._dump(data, 'WRITE')

        return self._write(data)

    def _dump(self, data, title):
        if len(data) == 0:
            return

        print '========== [{0}] =========='.format(title)

        length = 8
        line = 0
        while data:
            row = data[:length]
            data = data[length:]
            hex_data = ['%02X' % ord(byte) for byte in row]
            print '%04X' % line, ' '.join(hex_data)

        print ''

    def _open(self):
        raise DriverException("Not Implemented")

    def _close(self):
        raise DriverException("Not Implemented")

    def _read(self, count):
        raise DriverException("Not Implemented")

    def _write(self, data):
        raise DriverException("Not Implemented")

class USB1Driver(Driver):
    def __init__(self, device, baud_rate=115200, debug=False):
        Driver.__init__(self, device, debug)
        self.baud = baud_rate

    def _open(self):
        try:
            dev = serial.Serial(self.device, self.baud)
        except serial.SerialException, e:
            raise DriverException(str(e))

        if not dev.isOpen():
            raise DriverException('Could not open device')

        self._serial = dev
        self._serial.timeout = 0.01

    def _close(self):
        self._serial.close()

    def _read(self, count):
        return self._serial.read(count)

    def _write(self, data):
        try:
            count = self._serial.write(data)
            self._serial.flush()
        except serial.SerialTimeoutException, e:
            raise DriverException(str(e))

        return count
