# USB1 ANT stick interface. Running `dmesg | tail -n 25` after plugging the
# stick on a USB port should tell you the exact interface.
SERIAL = '/dev/ttyUSB0'

# If set to True, the stick's driver will dump everything it read/writes
# from/to the stick.
DEBUG = True
