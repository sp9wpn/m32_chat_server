# Simple transmitter
import socket
import logging
from mopp import * 
import config

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )

mopp = Mopp()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.connect((config.SERVER_IP, config.UDP_PORT))  # connect to the server

client_socket.send(mopp.mopp(20,'hi'))

client_socket.send(mopp.mopp(30,' hello world. this is a small test.'))
client_socket.send(mopp.mopp(10,'ok'))
