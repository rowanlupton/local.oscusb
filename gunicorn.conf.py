import multiprocessing
import os

# start usb keypress handler
from usb_osc import usbOSC
usbOSC()

bind = "unix:local.oscusb.sock"
workers = multiprocessing.cpu_count() * 2 + 1

