#!/usr/local/bin/python2.7
#
# https://github.com/sp9wpn/m32_chat_server
#
import socket
import time
from math import ceil

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


def str2hex(str):
  return ":".join("{:02x}".format(ord(c)) for c in str)

def mopp(speed,str):
  global serial

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

  for c in str:
    if c == " ":
      continue				# spaces not supported by morserino!

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


def stripheader(str):
  return chr(0x00) + chr(ord(str[1]) & 3) + str[2:]

def welcome(client, speed):
  ip,port = client.split(':')
  serversock.sendto(mopp(speed,':hi '+str(len(receivers))), (ip, int(port)))
  receivers[client] = time.time()
  debug("New client: %s" % client)

def reject(client, speed):
  ip,port = client.split(':')
  serversock.sendto(mopp(speed,':qrl'), (ip, int(port)))


while KeyboardInterrupt:
  time.sleep(0.2)						# anti flood
  try:
    data, addr = serversock.recvfrom(64)

    client = addr[0] + ':' + str(addr[1])

    debug ("\nReceived %s from %s" % (str2hex(data),client))

    speed = ord(data[1]) >> 2
    if client in receivers:
      if stripheader(data) == stripheader(mopp(20,':bye')):
        serversock.sendto(mopp(speed,':bye'), addr)
        del receivers[client]
        debug ("Removing client %s on request" % client)
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
      serversock.sendto(mopp(30,':bye'), (ip, int(port)))
      del receivers[c[0]]
      debug ("Removing expired client %s" % c[0])
 
