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

import thread

import serial

from ant.core.exceptions import DriverError


class Driver(object):
    _lock = thread.allocate_lock()

    def __init__(self, device, log=None, debug=False):
        self.device = device
        self.debug = debug
        self.log = log
        self.is_open = False

    def isOpen(self):
        self._lock.acquire()
        io = self.is_open
        self._lock.release()
        return io

    def open(self):
        self._lock.acquire()

        try:
            if self.is_open:
                raise DriverError("Could not open device (already open).")

            self._open()
            self.is_open = True
            if self.log:
                self.log.logOpen()
        finally:
            self._lock.release()

    def close(self):
        self._lock.acquire()

        try:
            if not self.is_open:
                raise DriverError("Could not close device (not open).")

            self._close()
            self.is_open = False
            if self.log:
                self.log.logClose()
        finally:
            self._lock.release()

    def read(self, count):
        self._lock.acquire()

        try:
            if not self.is_open:
                raise DriverError("Could not read from device (not open).")
            if count <= 0:
                raise DriverError("Could not read from device (zero request).")

            data = self._read(count)
            if self.log:
                self.log.logRead(data)

            if self.debug:
                self._dump(data, 'READ')
        finally:
            self._lock.release()

        return data

    def write(self, data):
        self._lock.acquire()

        try:
            if not self.is_open:
                raise DriverError("Could not write to device (not open).")
            if len(data) <= 0:
                raise DriverError("Could not write to device (no data).")

            if self.debug:
                self._dump(data, 'WRITE')

            ret = self._write(data)
            if self.log:
                self.log.logWrite(data[0:ret])
        finally:
            self._lock.release()

        return ret

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
        raise DriverError("Not Implemented")

    def _close(self):
        raise DriverError("Not Implemented")

    def _read(self, count):
        raise DriverError("Not Implemented")

    def _write(self, data):
        raise DriverError("Not Implemented")


class USB1Driver(Driver):
    def __init__(self, device, baud_rate=115200, log=None, debug=False):
        Driver.__init__(self, device, log, debug)
        self.baud = baud_rate

    def _open(self):
        try:
            dev = serial.Serial(self.device, self.baud)
        except serial.SerialException, e:
            raise DriverError(str(e))

        if not dev.isOpen():
            raise DriverError('Could not open device')

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
            raise DriverError(str(e))

        return count
