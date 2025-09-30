import json

from pythonosc import udp_client

def getch():
  import sys, tty, termios
  old_settings = termios.tcgetattr(0)
  new_settings = old_settings[:]
  new_settings[3] &= ~termios.ICANON
  try:
    termios.tcsetattr(0, termios.TCSANOW, new_settings)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(0, termios.TCSANOW, old_settings)
  return ch


while True:
  ch=getch()
  settings = 0;
  with open('settings.json', 'r') as f:
    settings = json.load(f)
    f.close()
  if (ch==' '):
    client = udp_client.SimpleUDPClient(settings['eos_ip'], settings['eos_port'])
    client.send_message(settings['osc_out'],100)
