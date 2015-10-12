#!/usr/bin/python
"""usb_unbind - uses the unbind/rebind sys-protocol, based on vendor-product ids."""

import sys
import argparse
from os.path import exists
from systools import sleep_with_countdown, find_bus_path, driver_path, bind, unbind

if __name__ == "__main__":
    # TODO: check for root
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("vendor", help="vendor id (or vendor:product)")
    parser.add_argument("product", help="product id", nargs="?")
    args = parser.parse_args()
    if not args.product:
        if ":" in args.vendor:
            args.vendor, args.product = args.vendor.split(":", 1)
        else:
            sys.exit("vendor product or vendor:product")

    syspath, systag = find_bus_path(bus="usb", idVendor=args.vendor, idProduct=args.product)
    driver = driver_path(syspath)
    assert exists(driver)
    print syspath
    raw_input("Press RETURN to unbind, sleep 5, and rebind: ")
    print "Unbinding", systag
    unbind(driver, systag)
    sleep_with_countdown(5)
    print "Rebinding", systag
    bind(driver, systag)
    sleep_with_countdown(3)
    print "DONE (but unchecked)"
