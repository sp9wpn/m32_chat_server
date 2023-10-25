#!/usr/local/bin/python3
# Receiver for UDP and publish to MQTT
import socket
import logging
import time
from mopp import * 
from paho import mqtt
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import config

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )

mopp = Mopp()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.connect((config.SERVER_IP, config.UDP_PORT))  # connect to the server

client_socket.send(mopp.mopp(20,'hi'))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    


last_r = {} # keep track of duplicate messages...

while KeyboardInterrupt:
  time.sleep(0.2)						# anti flood
  try:
    data_bytes, addr = client_socket.recvfrom(64)
    client = addr[0] + ':' + str(addr[1])
    r = mopp.decode_message(data_bytes)
    
    # Publish if message received
    if not "Keepalive" in r:
        if not last_r == r:
            print (r)
            msgs = [{'topic': "m32_test", 'payload': data_bytes}]
            publish.multiple(msgs, hostname=config.MQTT_HOST, port=config.MQTT_PORT, protocol=paho.MQTTv31)
            last_r = r
    
  except (KeyboardInterrupt, SystemExit):
    client_socket.close()
    break
    pass
