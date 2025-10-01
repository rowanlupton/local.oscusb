'''
this file contains a class which listens for specified keyboard input, and outputs OSC over network accordingly.
it takes settings from settings.json in the same directory (which is edited by the main Flask application)
we make use of threading in order to run this listener in the background, so that we can listen and serve a settings webpage simultaneously
'''

import json
from libinput import LibInput, ContextType, EventType, KeyState
from pythonosc import udp_client
from threading import Thread

# initialize libinput to listen to an available device
li = LibInput(context_type=ContextType.UDEV)
li.assign_seat('seat0')

class usbOSC(Thread):
  def __init__(self):
    # this calls our little listener in its own thread
    Thread.__init__(self)
    self.daemon = True
    self.start()
    
  def run(self):
    print('hello')
    # for each key press we hear
    for event in li.events:
      # this opens our settings.json into the settings variable
      with open('settings.json', 'r') as f:
        settings = json.load(f)

      # if we're listening to a keyboard
      if event.type.is_keyboard():
        # if the key pressed matches the key we defined in our settings json file
        if event.key == int(settings['input_value']['value']):
          # the int() function is necessary because updating settings makes
          # everything into a string, and event.key is an int.
          # int() appears a few times here for the same reason

          # define OSC UDP client using settings from our json
          client = udp_client.SimpleUDPClient(settings['eos_ip']['value'], int(settings['eos_port']['value']))
          
          # the below line is required to use faders over OSC.
          # working on a more elegant and flexible solution.
          try:
            client.send_message('/eos/fader/1/config/10','')
          except Exception as e:
            print(f"Error: an unhandled error occurred - {e}")
            
          if event.key_state == KeyState.PRESSED:
            
            # send the actual OSC string to EOS
            try:
              client.send_message(settings['osc_out']['value'],settings['osc_arg']['value'])
            except Exception as e:
              print(f"Error: an unhandled error occurred - {e}")
            
          elif event.key_state == KeyState.RELEASED and settings['osc_arg_release']['value'] != "":
            try:
              client.send_message(settings['osc_out']['value'],settings['osc_arg_release']['value'])
            except Exception as e:
              print(f"Error: an unhandled error occurred - {e}")
