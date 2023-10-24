import ssl
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
from paho import mqtt
from hivemq import *

from mopp import * 
from beep import *

mopp = Mopp()

# callback to print a message once it arrives
def print_msg(client, userdata, message):
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param message: the message with topic and payload
    """
    print("%s : %s" % (message.topic, message.payload))
    r = mopp.decode_message(message.payload)
    print (r)

    # Beep if message received
    if not "Keepalive" in r:
        b = Beep(speed=r["Speed"])
        b.beep_message(r["Message"])



sslSettings = ssl.SSLContext(mqtt.client.ssl.PROTOCOL_TLS)
auth = {'username': user, 'password': pw}
subscribe.callback(print_msg, "#", hostname=host, port=8883, auth=auth, tls=sslSettings, protocol=paho.MQTTv31)


