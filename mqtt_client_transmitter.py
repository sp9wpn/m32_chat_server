#!/usr/local/bin/python3
# Simple transmitter

import paho.mqtt.client as paho
import logging
from mopp import * 
import config

logging.basicConfig(level=logging.DEBUG, format='%(message)s', )

mopp = Mopp()



def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    r = mopp.decode_message(msg.payload)
    print (r)

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass

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
mqttc.loop_start()

infot = mqttc.publish("m32_test", mopp.mopp(20,'hi'), qos=2)
#infot = mqttc.publish("m32_test", mopp.mopp(20,'hihio'), qos=2)
infot = mqttc.publish("m32_test", mopp.mopp(20,'hi'), qos=2)
infot = mqttc.publish("m32_test", mopp.mopp(20,'m'), qos=2)
#infot = mqttc.publish("m32_test", mopp.mopp(20,'this is a test'), qos=2)

infot.wait_for_publish()

