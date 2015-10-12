#!/usr/bin/python
"""usb_reset - does a USBDEVFS_RESET on a device, causing automatic re-enumeration.

WARNING: reset'ing some devices appears to only make things
worse, so this currently is a last resort.
"""

import os
import sys
import argparse
import fcntl
from systools import find_usb_bus_from_id

# Values (facts) from linux/usbdevice_fs.h and asm-generic/ioctl.h from linux-libc-dev.

_ioc_none      = 0
_ioc_nrshift   = 0
_ioc_nrbits    = 8
_ioc_typeshift = (_ioc_nrshift+_ioc_nrbits)
_ioc_typebits  = 8
_ioc_sizeshift = (_ioc_typeshift+_ioc_typebits)
_ioc_sizebits  = 14
_ioc_dirshift  = (_ioc_sizeshift+_ioc_sizebits)

def _IOC(DIR,TYPE,NR,SIZE):
    return ((DIR  << _ioc_dirshift)  |
            (TYPE << _ioc_typeshift) |
            (NR   << _ioc_nrshift)   |
            (SIZE << _ioc_sizeshift))

def _IO(TYPE,NR):
    return _IOC(_ioc_none,TYPE,NR,0)

USBDEVFS_RESET = _IO(ord('U'), 20)

if __name__ == "__main__":
    # TODO: check for root
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    identifier = parser.add_mutually_exclusive_group(required=True)
    identifier.add_argument("--path", help="raw /dev/bus/usb path (use the other args instead)")
    identifier.add_argument("--bus", help="bus-id dev-id", type=int, nargs=2, metavar=("BUS", "DEV"))
    identifier.add_argument("--vendor", help="vendor:product device *class*, use the first one found")
    args = parser.parse_args()

    if args.path:
        path = args.path
    elif args.bus:
        path = "/dev/bus/usb/{:03d}/{:03d}".format(*args.bus)
    elif args.vendor:
        assert args.vendor.count(":") == 1, "vendor:product (like 1d27:0601)"
        bus, dev = find_usb_bus_from_id(*args.vendor.split(":"))
        path = "/dev/bus/usb/{:03d}/{:03d}".format(bus, dev)
        # consider pulling DEVNAME=bus/usb/002/004$ from /uevent instead...

    fd = os.open(path, os.O_WRONLY)
    rc = fcntl.ioctl(fd, USBDEVFS_RESET, 0)
    os.close(fd)
    if rc == 0:
        print "Reset of", path, "complete"
    else:
        # if *errno* is set, we'll have already gotten an exception...
        sys.exit("ioctl returned {}".format(rc))
