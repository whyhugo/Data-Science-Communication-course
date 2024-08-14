import paho.mqtt.client as mqtt
import ssl
import struct
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code = "+str(rc))

def on_message(client, userdata, msg):
    print(str(msg.payload, encoding='utf8'))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "whyhugo")
client.on_connect = on_connect
client.on_message = on_message

#TODO: use the username and password for your group
client.username_pw_set(config['NTNUpw']['username'], config['NTNUpw']['password'])
client.connect("140.122.185.98", 1883, 60) #localhost

client.loop_start()
time.sleep(1)
print("Enter topic-to-subscribe: ", end='')
tp_sub = input()
client.subscribe(tp_sub, 0)
print("Enter topic-to-publish: ", end='')
tp_pub = input()
while True:
    msg = input()
    client.publish(tp_pub, msg, 0)
client.loop_stop()
