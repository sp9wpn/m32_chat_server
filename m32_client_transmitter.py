#!/usr/local/bin/python3
import socket
import logging
from mopp import * 

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )

SERVER_IP = "0.0.0.0"
UDP_PORT = 7373

mopp = Mopp()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.connect((SERVER_IP, UDP_PORT))  # connect to the server

client_socket.send(mopp.mopp(20,'hi'))

client_socket.send(mopp.mopp(30,' hello world. this is a small test.'))
