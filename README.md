# linux-bus-reset-tools

Tools that reset specific interfaces, helpful for avoiding physically unplugging remote or embedded devices.

They need to run as root, and are somewhat indiscriminate - remember
that the bus they're resetting might include your keyboard or network
controller, and be prepared to have to reboot your system by other
means; these are tools that *might* save you a reboot, but you're
using them because things have already gone wrong, so don't expect too
much.

## pci_reset

    usage: pci_reset.py [-h] [--pci-bus PCI_BUS] [--pci-id PCI_ID] [--usb2] [--usb3]
    
    pci_reset - does an unbind/bind of an entire device
    
    optional arguments:
      -h, --help            show this help message and exit
      --pci-bus PCI_BUS
      --pci-id PCI_ID, -s PCI_ID
                            raw PCI id (no checking)
      --usb2, -2            Find one usb2(ehci) controller and whack it
      --usb3, -3            Find one usb3(xhci) controller and whack it

## usb_reset

    usage: usb_reset.py [-h] (--path PATH | --bus BUS DEV | --vendor VENDOR)
    
    usb_reset - does a USBDEVFS_RESET on a device, causing automatic re-enumeration.
    
    WARNING: reset'ing some devices appears to only make things
    worse, so this currently is a last resort.
    
    optional arguments:
      -h, --help       show this help message and exit
      --path PATH      raw /dev/bus/usb path (use the other args instead)
      --bus BUS DEV    bus-id dev-id
      --vendor VENDOR  vendor:product device *class*, use the first one found

## usb_unbind

    usage: usb_unbind.py [-h] vendor [product]
    
    usb_unbind - uses the unbind/rebind sys-protocol, based on vendor-product ids.
    
    positional arguments:
      vendor      vendor id (or vendor:product)
      product     product id
    
    optional arguments:
      -h, --help  show this help message and exit
