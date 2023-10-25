# Simple receiver

import socket
import logging
import time
from mopp import * 
from beep import *
import config

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )


mopp = Mopp()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.connect((config.SERVER_IP, config.UDP_PORT))  # connect to the server

client_socket.send(mopp.mopp(20,'hi'))

last_r = {} # keep track of duplicate messages...

while KeyboardInterrupt:
  time.sleep(0.2)						# anti flood
  try:
    data_bytes, addr = client_socket.recvfrom(64)
    client = addr[0] + ':' + str(addr[1])
    r = mopp.decode_message(data_bytes)
    print (r)
    
    # Beep if message received
    if not "Keepalive" in r:
        b = Beep(speed=r["Speed"])
        if not last_r == r:
            b.beep_message(r["Message"])
            last_r = r
    


  except (KeyboardInterrupt, SystemExit):
    client_socket.close()
    break
    pass
