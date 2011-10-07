ANT
===

Introduction
------------
Python implementation of the ANT, ANT+, and ANT-FS protocols. For more
information about ANT, see http://www.thisisant.com/.

Can be used to communicate with ANT nodes using an ANT stick (USB).

This project came to be when I tried to download data for analysis from my
ANT+/ANT-FS enabled running watch under GNU/Linux. This eventually lead me to
attempting to port ANT_LIB and ANT_DLL (by Dynastream) to Linux. However, I
didn't quite like the library, the protocol is well documented and trivial to
implement, and I was going to have to write a ctypes-based wrapper afterwards
since I was only going to use the library from Python. Thus, I decided to
write a pure Python implementation.


Contact
-------
You can reach me via e-Mail and Google Talk/Jabber at:
    martin at NOSPAM martinvillalba dot com

Documentation
-------------
Documentation will be a bit scarse for the time being, but everything public
should have at least a docstring by the time I make the first stable release.


License
-------
Released under the MIT/X11 license. See LICENSE for the full text.


Install
-------
% python setup.py install


Develop
-------
See DEVELOP.md for details.
