#!/usr/local/bin/python3
# Subscriber for MQTT with Morse Code Beep

import paho.mqtt.client as paho
import config

from mopp import * 
from beep import *

mopp = Mopp()

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    r = mopp.decode_message(msg.payload)
    print (r)

    # Beep if message received
    if not "Keepalive" in r:
        b = Beep(speed=r["Speed"])
        b.beep_message(r["Message"])

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)


mqttc = paho.Client()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect(config.MQTT_HOST, config.MQTT_PORT, 60)
mqttc.subscribe("m32_test", 0)

mqttc.loop_forever()
