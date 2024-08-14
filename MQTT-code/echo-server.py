import paho.mqtt.client as mqtt
import ssl
import struct
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

to_client = "123a"
to_server = "b123"

def on_message(client, userdata, msg):
    payload_string = str(msg.payload, encoding='utf8')
    print("Received (topic '" + msg.topic + "'): " + payload_string)
    time.sleep(1)
    client.publish(to_client, "server: You typed '" + payload_string +"'", 0)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"")
client.on_message = on_message
#TODO: Use the username and password for your group
client.username_pw_set(config['NTNUpw']['username'], config['NTNUpw']['password'])
print("This runs a simple server to echo client string.")
client.connect("140.122.185.98", 1883, 60)
client.subscribe(to_server, 0)
client.loop_forever()
