#!/usr/bin/python

"""Helper functions for device-interface kernel-tweaking tools"""

import sys
import time
import subprocess
from os import listdir
from os.path import join, exists, realpath

def lspci():
    lspci_txt = subprocess.check_output(["lspci", "-vmm"])
    slots = {}
    current = {}
    for line in lspci_txt.splitlines():
        if not line.strip():
            slots[current["slot"]] = current
            current = {}
        else:
            tag, _, val = line.partition(":\t")
            current[tag.lower()] = val
    return slots

def lspci_lookup(pci_classname, in_description):
    for slot, record in lspci().items():
        if record["class"] == pci_classname and in_description in record["device"]:
            return slot
    raise ValueError("{}/{} not found".format(pci_classname, in_description))

def find_bus_path(bus, **kwargs):
    buspath = "/sys/bus/{}/devices".format(bus)
    for devname in listdir(buspath):
        devp = join(buspath, devname)
        for tagname, tagvalue in kwargs.items():
            tagp = join(devp, tagname)
            if not exists(tagp) or not tagvalue == file(tagp).read().strip():
                break
        else: # all the tags matched...
            return devp, devname

def read_int(path):
    return int(file(path).read().strip())

def find_usb_bus_from_id(vendor, product):
    syspath, systag = find_bus_path("usb", idVendor=vendor, idProduct=product)
    # TODO: only works for trivial paths, but so does /dev/bus/usb...
    return read_int(join(syspath, "busnum")), read_int(join(syspath, "devnum"))

def driver_path(buspath):
    assert exists(buspath)
    assert exists(join(buspath, "driver"))
    return realpath(join(buspath, "driver"))

def bind(driver, systag, verb="bind"):
    with file(join(driver, verb), "w") as drf:
        print >> drf, systag

def unbind(driver, systag):
    return bind(driver, systag, verb="unbind")


def sleep_with_countdown(seconds):
    for i in range(seconds,0,-1):
        sys.stdout.write("{}... ".format(i))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\n")

