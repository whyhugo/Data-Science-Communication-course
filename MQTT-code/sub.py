# The following example is derived from
# the official example at https://pypi.org/project/paho-mqtt/
import paho.mqtt.client as mqtt
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def on_message(client, userdata, msg):
    payload_string = str(msg.payload, encoding='utf8')
    print(payload_string)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"sub") #TODO: update this to a unique name
client.on_message = on_message
#TODO: Use the username and password for your group
client.username_pw_set(config['NTNUpw']['username'], config['NTNUpw']['password'])
print("A simple subscriber.")
client.connect("140.122.185.98", 1883, 60)
client.subscribe("example-topic", 0)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_forever()
