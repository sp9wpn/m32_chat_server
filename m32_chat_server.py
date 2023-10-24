#!/usr/local/bin/python3
import socket
import time
import logging
from math import ceil
from mopp import * 

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )

SERVER_IP = "0.0.0.0"
UDP_PORT = 7373
CLIENT_TIMEOUT = 300
MAX_CLIENTS = 10
KEEPALIVE = 10
DEBUG = 0
MY_WPM = 20

serversock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serversock.bind((SERVER_IP, UDP_PORT))
serversock.settimeout(KEEPALIVE)

receivers = {}
mopp = Mopp()

def transmit (data, ip, port):
  serversock.sendto(data, (ip, int(port)))

def broadcast(data,client):
  for c in receivers.keys():
    if c == client:
      continue
    logging.debug("Sending to %s" % c)
    ip,port = c.split(':')

    transmit (data, ip, port)

def welcome(client, speed):
  ip,port = client.split(':')
  welcome_msg = ':hi '+str(len(receivers))
  transmit(mopp.mopp(speed, welcome_msg), ip, port)
  receivers[client] = time.time()
  logging.debug("New client: %s" % client)

def reject(client, speed):
  ip,port = client.split(':')
  bye_msg = ':qrl'
  transmit(mopp.mopp(speed, bye_msg), ip, int(port))

while KeyboardInterrupt:
  time.sleep(0.2)						# anti flood
  try:
    data_bytes, addr = serversock.recvfrom(64)
    client = addr[0] + ':' + str(addr[1])
    speed = mopp.received_speed(data_bytes)
    logging.debug ("\nReceived %s from %s with %i wpm" % (mopp.received_data(data_bytes),client, speed)) 

    if client in receivers:
      if mopp.msg_strcmp(data_bytes, MY_WPM, ':bye'):
        serversock.sendto(mopp.mopp(speed,':bye'), addr) # FIXME
        del receivers[client]
        logging.debug ("Removing client %s on request" % client)
      else:
        broadcast (data_bytes, client)
        receivers[client] = time.time()
    else:
      if mopp.msg_strcmp(data_bytes, MY_WPM, 'hi'):
        if (len(receivers) < MAX_CLIENTS):
          receivers[client] = time.time()
          welcome(client, speed)
        else:
          reject(client, speed)
          logging.debug ("ERR: maximum clients reached")
      else:
        logging.debug ("-unknown client, ignoring-")

  except socket.timeout:
    # Send UDP keepalives
    for c in receivers.keys():
      ip,port = c.split(':')
      serversock.sendto(bytes('','utf-8'), (ip, int(port)))
    pass

  except (KeyboardInterrupt, SystemExit):
    serversock.close()
    break
    pass

  # clean clients list
  for c in receivers.items():
    if c[1] + CLIENT_TIMEOUT < time.time():
      ip,port = c[0].split(':')
      bye_msg = ':bye'
      transmit(mopp.mopp(MY_WPM, bye_msg), ip, int(port))
      del receivers[c[0]]
      logging.debug ("Removing expired client %s" % c[0])
 