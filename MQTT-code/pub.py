# The following example is derived from
# the official example at https://pypi.org/project/paho-mqtt/
import paho.mqtt.client as mqtt
import sys
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"whyhugo") #TODO: update this to a unique name
#TODO: Use the username and password for your group
client.username_pw_set(config['NTNUpw']['username'], config['NTNUpw']['password'])
client.connect("140.122.185.98", 1883, 60) 
#client.connect("localhost", 1883, 60)

msg = sys.argv[1]
client.publish("example-topic", msg, 0)
print("Publishing message '" + msg + "'")
