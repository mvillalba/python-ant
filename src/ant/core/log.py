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
import datetime

import msgpack

EVENT_OPEN=0x01
EVENT_CLOSE=0x02
EVENT_READ=0x03
EVENT_WRITE=0x04

class LogReader(object):
    def __init__(self, filename):
        self.is_open = False
        self.open(filename)

    def __del__(self):
        if self.is_open:
            self.fd.close()

    def open(self, filename):
        if self.is_open == True:
            self.close()

        self.fd = open(filename, 'r')
        self.is_open = True
        self.unpacker = msgpack.Unpacker()

        # Here be dragons
        self.unpacker.feed(self.fd.read())
        self.fd.close()

        header = self.unpacker.unpack()
        if len(header) != 2 or header[0] != 'ANT-LOG' or header[1] != 0x01:
            raise IOError('Could not open log file (unknown format).')

    def close(self):
        if self.is_open:
            self.fd.close()
            self.is_open = False

    def read(self):
        try:
            return self.unpacker.unpack()
        except StopIteration:
            return None

class LogWriter(object):
    def __init__(self, filename=''):
        self.packer = msgpack.Packer()
        self.is_open = False
        self.open(filename)

    def __del__(self):
        if self.is_open:
            self.fd.close()

    def open(self, filename=''):
        if filename == '':
            filename = datetime.datetime.now().isoformat() + '.ant'

        if self.is_open == True:
            self.close()

        self.fd = open(filename, 'w')
        self.is_open = True
        self.packer = msgpack.Packer()

        header = ['ANT-LOG', 0x01] # [MAGIC, VERSION]
        self.fd.write(self.packer.pack(header))

    def close(self):
        if self.is_open:
            self.fd.close()
            self.is_open = False

    def logOpen(self):
        ev_open = [EVENT_OPEN, int(time.time())]
        self.fd.write(self.packer.pack(ev_open))

    def logClose(self):
        ev_close = [EVENT_CLOSE, int(time.time())]
        self.fd.write(self.packer.pack(ev_close))

    def logRead(self, data):
        if len(data) == 0:
            return

        ev_read = [EVENT_READ, int(time.time()), data]
        self.fd.write(self.packer.pack(ev_read))

    def logWrite(self, data):
        if len(data) == 0:
            return

        ev_write = [EVENT_WRITE, int(time.time()), data]
        self.fd.write(self.packer.pack(ev_write))

