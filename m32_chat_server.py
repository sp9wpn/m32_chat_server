#!/usr/local/bin/python3
import socket
import time
import logging
from math import ceil

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )

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

serial = 1

def broadcast(data,client):
  for c in receivers.keys():
    if c == client:
      continue
    logging.debug("Sending to %s" % c)
    ip,port = c.split(':')

    serversock.sendto(data, (ip, int(port)))


def str2hex(bytes):
  msg = bytes.decode()
  hex = ":".join("{:02x}".format(ord(c)) for c in msg)
  return hex

def mopp(speed,msg):
  global serial

  logging.debug("Encoding message with "+str(speed)+" wpm :"+str(msg))

  morse = {
	"0" : "-----", "1" : ".----", "2" : "..---", "3" : "...--", "4" : "....-", "5" : ".....",
	"6" : "-....", "7" : "--...", "8" : "---..", "9" : "----.",
	"a" : ".-", "b" : "-...", "c" : "-.-.", "d" : "-..", "e" : ".", "f" : "..-.", "g" : "--.",
	"h" : "....", "i" : "..", "j" : ".---", "k" : "-.-", "l" : ".-..", "m" : "--", "n" : "-.",
	"o" : "---", "p" : ".--.", "q" : "--.-", "r" : ".-.", "s" : "...", "t" : "-", "u" : "..-",
	"v" : "...-", "w" : ".--", "x" : "-..-", "y" : "-.--", "z" : "--..", "=" : "-...-",
	"/" : "-..-.", "+" : ".-.-.", "-" : "-....-", "." : ".-.-.-", "," : "--..--", "?" : "..--..",
	":" : "---...", "!" : "-.-.--", "'" : ".----."
  }

  m = '01'				# protocol
  m += bin(serial)[2:].zfill(6)
  m += bin(speed)[2:].zfill(6)

  for c in msg:
    if c == " ":
      continue				# spaces not supported by morserino!

    logging.debug(c)
    
    for b in morse[c.lower()]:
      if b == '.':
        m += '01'
      else:
        m += '10'

    m += '00'				# EOC

  m = m[0:-2] + '11'			# final EOW

  m = m.ljust(int(8*ceil(len(m)/8.0)),'0')

  res = ''
  for i in range (0, len(m), 8):
    res += chr(int(m[i:i+8],2))

  serial += 1
  return res

def stripheader(msg):
  res = chr(0x00) + chr(ord(msg[1]) & 3) + msg[2:]
  return res

def welcome(client, speed):
  ip,port = client.split(':')
  welcome_msg = ':hi '+str(len(receivers))
  serversock.sendto(bytes(mopp(speed, welcome_msg),'utf-8'), (ip, int(port)))
  receivers[client] = time.time()
  logging.debug("New client: %s" % client)

def reject(client, speed):
  ip,port = client.split(':')
  bye_msg = ':qrl'
  serversock.sendto(bytes(mopp(speed, bye_msg),'utf-8'), (ip, int(port)))


while KeyboardInterrupt:
  time.sleep(0.2)						# anti flood
  try:
    data_bytes, addr = serversock.recvfrom(64)
    client = addr[0] + ':' + str(addr[1])
    data = data_bytes.decode()
    speed = ord(data[1]) >> 2
    logging.debug ("\nReceived %s from %s with %i wpm" % (str2hex(data_bytes),client, speed))

    if client in receivers:
      if stripheader(data) == stripheader(mopp(20,':bye')):
        serversock.sendto(bytes(mopp(speed,':bye'),'utf-8'), addr)
        del receivers[client]
        logging.debug ("Removing client %s on request" % client)
      else:
        broadcast (data, client)
        receivers[client] = time.time()
    else:
      if stripheader(data) == stripheader(mopp(20,'hi')):
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
      my_speed = 30
      serversock.sendto(bytes(mopp(my_speed, bye_msg),'utf-8'), (ip, int(port)))
      del receivers[c[0]]
      logging.debug ("Removing expired client %s" % c[0])
 