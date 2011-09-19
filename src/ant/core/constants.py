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

MESSAGE_TX_SYNC = 0xA4

# Configuration messages
MESSAGE_CHANNEL_UNASSIGN = 0x41
MESSAGE_CHANNEL_ASSIGN = 0x42
MESSAGE_CHANNEL_ID = 0x51
MESSAGE_CHANNEL_PERIOD = 0x43
MESSAGE_CHANNEL_SEARCH_TIMEOUT = 0x44
MESSAGE_CHANNEL_FREQUENCY = 0x45
MESSAGE_CHANNEL_TX_POWER = 0x60
MESSAGE_NETWORK_KEY = 0x46
MESSAGE_TX_POWER = 0x47
MESSAGE_PROXIMITY_SEARCH = 0x71

# Notification messages
MESSAGE_STARTUP = 0x6F

# Control messages
MESSAGE_SYSTEM_RESET = 0x4A
MESSAGE_CHANNEL_OPEN = 0x4B
MESSAGE_CHANNEL_CLOSE = 0x4C
MESSAGE_CHANNEL_REQUEST = 0x4D

# Data messages
MESSAGE_CHANNEL_BROADCAST_DATA = 0x4E
MESSAGE_CHANNEL_ACKNOWLEDGED_DATA = 0x4F
MESSAGE_CHANNEL_BURST_DATA = 0x50

# Channel event messages
MESSAGE_CHANNEL_EVENT = 0x40

# Requested response messages
MESSAGE_CHANNEL_STATUS = 0x52
#MESSAGE_CHANNEL_ID = 0x51
MESSAGE_VERSION = 0x3E
MESSAGE_CAPABILITIES = 0x54
MESSAGE_SERIAL_NUMBER = 0x61
