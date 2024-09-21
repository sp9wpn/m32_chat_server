#!/usr/local/bin/python3
# The MOPP Chat Client (UDP)

import socket
import time
import logging
from mopp import * 
import argparse
import threading
import os

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )

argparser = argparse.ArgumentParser(description='MOPP - IP/UDP console client')
argparser.add_argument('server', help='Server IP or hostname')
argparser.add_argument('port', help='Server UDP port (default: 7373)', nargs='?', type=int, default=7373)

args=argparser.parse_args()

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(0.2)

speed = 20

mopp = Mopp()

def transmit (data):
  if len(data) > 0:
    sock.sendto(data, (socket.gethostbyname(args.server), args.port))


def inputThread():
  global speed

  while True:
    i = input().strip()
    if i == '#quit':
      transmit(mopp.mopp(speed, ':bye'))
      print("Quitting...")
      os._exit(0)
      break

    if i[0:1] == '#':
      try:
        _speed = int(i[1:])
        if (_speed >= 5 and _speed <= 60):
          speed = _speed
          print("Speed set to %d wpm." % speed) 
        else:
          print("Allowed speeds from 5 to 60 wpm.")

      except:
        pass

      continue

    for word in i.split(' '):
      if word != '':
        # print("Transmitting (%d wpm): %s" % (speed,word))
        transmit(mopp.mopp(speed, word))



print("### MOPP - IP/UDP console client")
print("### Speed is set to %d wpm. To change, type: #<wpm>" % speed)
print("### To exit the program, use #quit")
print("")

# Login with hi
transmit(mopp.mopp(speed, 'hi'))


iThread = threading.Thread(target=inputThread)
iThread.daemon = True
iThread.start()


while KeyboardInterrupt:
  try:
    data_bytes, addr = sock.recvfrom(64)
    try:
      if len(data_bytes) > 0:
        r = mopp.decode_message(data_bytes)
        print ("Received (%d wpm): %s" % (mopp.received_speed(data_bytes), r['Text']))
    except:
      raise
      pass

  except (KeyboardInterrupt, SystemExit):
    transmit(mopp.mopp(speed, ':bye'))
    sock.close()
    break
    pass

  except socket.timeout:
    pass

