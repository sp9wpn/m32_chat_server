#!/usr/local/bin/python3
# The MOPP Chat Client (UDP)

import socket
import time
import logging
from mopp import * 
import config
import argparse
import sys
import select

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )

argparser = argparse.ArgumentParser(description='MOPP - IP/UDP console client')
argparser.add_argument('ip', help='Server IP address')
argparser.add_argument('port', help='Server UDP port (default: 7373)', nargs='?', type=int, default=7373)

args=argparser.parse_args()

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(0.2)

speed = 20

mopp = Mopp()

def transmit (data):
  if len(data) > 0:
    sock.sendto(data, (args.ip, args.port))

print("### MOPP - IP/UDP console client")
print("### Speed is set to %d wpm. To change, type: #<wpm>" % speed)
print("")

# Login with hi
transmit(mopp.mopp(speed, 'hi'))


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
    sock.close()
    break
    pass

  except socket.timeout:
    # time.sleep(0.2)						# anti flood
    pass

  _i, _o, _e = select.select([sys.stdin], [], [], 1)
  if (_i):
    input = sys.stdin.readline().strip()

    if input[0:1] == '#':
      try:
        _speed = int(input[1:])
        if (_speed >= 5 and _speed <= 60):
          speed = _speed
          print("Speed set to %d wpm." % speed) 
        else:
          print("Allowed speeds from 5 to 60 wpm.")

      except:
        pass

      continue

    for word in input.split(' '):
      if word != '':
        # print("Transmitting (%d wpm): %s" % (speed,word))
        transmit(mopp.mopp(speed, word))
