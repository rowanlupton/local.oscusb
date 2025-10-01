from app import app
from usb_osc import usbOSC

def server():
    usbOSC()
    app.run()
