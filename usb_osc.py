'''
this file contains a class which listens for specified keyboard input, and outputs OSC over network accordingly.
it takes settings from settings.json in the same directory (which is edited by the main Flask application)
we make use of threading in order to run this listener in the background, so that we can listen and serve a settings webpage simultaneously
'''

import json
from libinput import LibInput, ContextType, EventType, KeyState
from pythonosc import udp_client
from threading import Thread

li = LibInput(context_type=ContextType.UDEV)
li.assign_seat('seat0')

class usbOSC(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.daemon = True
    self.start()
  def run(self):
    settings = 0
    for event in li.events:
      with open('settings.json', 'r') as f:
        settings = json.load(f)
      f.close()
          
      if event.type.is_keyboard() and event.key_state == KeyState.PRESSED:
        print(event.device)
        if event.key == settings['input_value']['value']:
          print('go:',event.key_state)
          
          client = udp_client.SimpleUDPClient(settings['eos_ip']['value'], settings['eos_port']['value'])
          client.send_message('/eos/fader/1/config/10','')
          client.send_message(settings['osc_out']['value'],settings['osc_arg']['value'])
        else:
          print('wrong input')
      elif event.type.is_keyboard() and event.key_state == KeyState.RELEASED:
        print('release')

