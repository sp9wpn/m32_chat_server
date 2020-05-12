#!/usr/bin/python2.7
#
# https://github.com/sp9wpn/m32_chat_server
#
import socket
import time
 
SERVER_IP = "0.0.0.0"
UDP_PORT = 7373
CLIENT_TIMEOUT = 300
MAX_CLIENTS = 10
KEEPALIVE = 10
DEBUG = 0
 
serversock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serversock.bind((SERVER_IP, UDP_PORT))
serversock.settimeout(KEEPALIVE)

receivers = {}



def debug(str):
  if DEBUG:
    print str

def broadcast(data,client):
  for c in receivers.keys():
    if c == client:
      continue
    debug("Sending to %s" % c)
    ip,port = c.split(':')

    serversock.sendto(data, (ip, int(port)))


def welcome(client):
  ip,port = client.split(':')
  serversock.sendto('D\x7a\xa5\x45\x51\x70', (ip, int(port)))		# this is ":hi" at 30wpm
  receivers[client] = time.time()
  debug("New client: %s" % client) 

 
while KeyboardInterrupt:
  time.sleep(0.2)						# anti flood
  try:
    data, addr = serversock.recvfrom(64)
  
    client = addr[0] + ':' + str(addr[1])

    debug ("\nReceived %s from %s" % (":".join("{:02x}".format(ord(c)) for c in data),client))

    if client in receivers:
      broadcast (data, client)
      receivers[client] = time.time()
    else:
      if data[2:4] == 'T\\':
        if (len(receivers) < MAX_CLIENTS):
          receivers[client] = time.time()
          welcome(client)
        else:
          debug ("ERR: maximum clients reached")
      else:
        debug ("-unknown client, ignoring-")

  except socket.timeout:
    # Send UDP keepalives
    for c in receivers.keys():
      ip,port = c.split(':')
      serversock.sendto('', (ip, int(port)))
    pass

  except (KeyboardInterrupt, SystemExit):
    serversock.close()
    break
    pass
 

  # clean clients list
  for c in receivers.items():
    if c[1] + CLIENT_TIMEOUT < time.time():
      ip,port = c[0].split(':')
      serversock.sendto('D\x7a\xa5\x49\x52\x68\x70', (ip, int(port)))		# this is ":bye" at 30wpm
      del receivers[c[0]]
      debug ("Removing expired client %s" % c[0])

