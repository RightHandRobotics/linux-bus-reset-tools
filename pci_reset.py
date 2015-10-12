#!/usr/bin/python
"""pci_reset - does an unbind/bind of an entire device"""

import sys
import argparse
import os
from os.path import realpath
from systools import sleep_with_countdown, lspci, lspci_lookup, bind, unbind

if __name__ == "__main__":
    ## let's restrict ourselves to USB controllers for now...
    # 00:14.0 USB controller: Intel Corporation Wildcat Point-LP USB xHCI Controller (rev 03)
    # 00:1d.0 USB controller: Intel Corporation Wildcat Point-LP USB EHCI Controller (rev 03)
    # UHCI: USB 1.x
    # EHCI: USB 2.0
    # XHCI: USB 3.x
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pci-bus", default="0000")
    parser.add_argument("--pci-id", "-s", help="raw PCI id (no checking)")
    parser.add_argument("--usb2", "-2", action="store_true", help="Find one usb2(ehci) controller and whack it")
    parser.add_argument("--usb3", "-3", action="store_true", help="Find one usb3(xhci) controller and whack it")
    args = parser.parse_args()

    if args.pci_id:
        if args.usb2 or args.usb3:
            sys.exit("id *or* controller, not both")
        pci_id = args.pci_id
        slots = lspci().keys()
        if pci_id not in slots:
            sys.exit("{} not found in {!r}".format(pci_id, slots))
    elif args.usb2:
        if args.usb3:
            sys.exit("only reset one controller at a time")
        pci_id = lspci_lookup("USB controller", "EHCI") # class 0x0c03
    elif args.usb3:
        if args.usb2:
            sys.exit("only reset one controller at a time")
        pci_id = lspci_lookup("USB controller", "xHCI") # class 0x0c03
    else:
        sys.exit("specify some pci slot")

    full_pci_id = "{}:{}".format(args.pci_bus, pci_id)
    print "id:", full_pci_id
    driver = realpath("/sys/bus/pci/devices/{}/driver".format(full_pci_id))
    print "driver:", driver
    assert os.path.exists(driver), "{} not found".format(driver)
    raw_input("Press RETURN to unbind, sleep 5, and rebind: ")
    print "Unbinding", full_pci_id
    unbind(driver, full_pci_id)
    sleep_with_countdown(5)
    print "Rebinding", full_pci_id
    bind(driver, full_pci_id)
    sleep_with_countdown(3)
    print lspci().get(pci_id, "{} not found after rebind!".format(pci_id))

    # TODO: catch any added lines in kern.log for signs of activity
