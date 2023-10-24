#!/usr/local/bin/python3
import socket
import time
import logging
from math import ceil

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )


SERVER_IP = "0.0.0.0"
UDP_PORT = 7373

serial = 1


def str2hex(bytes):
  #msg = bytes.decode()
  #hex = ":".join("{:02x}".format(ord(c)) for c in msg)
  hex = ":".join("{:02x}".format(c) for c in bytes)
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

    #logging.debug(c)
    
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
  return bytes(res,'utf-8')

def stripheader(msg):
  #logging.debug(msg)
  #logging.debug(type(msg))
  #res = chr(0x00) + chr(msg[1] & 3) + msg[2:]
  res = bytes(0x00) + bytes(msg[1] & 3) + msg[2:]
  return res



client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.connect((SERVER_IP, UDP_PORT))  # connect to the server

client_socket.send(mopp(20,'hi'))

client_socket.send(mopp(20,' hello world. this is a small test.'))
