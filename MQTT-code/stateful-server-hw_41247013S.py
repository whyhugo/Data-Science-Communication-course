import paho.mqtt.client as mqtt
import ssl
import struct
import time
import random
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

magic_list = []
to_client = "123a"
to_server = "b123"

def on_connect(client, userdata, flags, rc, properties):
    print("Connected to the broker.")

def on_message(client, userdata, msg):
    payload_string = str(msg.payload, encoding='utf8')
    time.sleep(1)
    global magic_list
    match payload_string:
        case "menu":
            client.publish(to_client, "\
                --- menu ---\n\
                0: Get the server local time\n\
                1: Show the current content of the magic list\n\
                2: Append a random integer to the magic list", 0)
        case "0":
            client.publish(to_client, time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime(time.time())))
        case "1":
            client.publish(to_client, str(magic_list))
        case "2":
            random_integer = random.randint(1, 100)
            magic_list.append(random_integer)
            client.publish(to_client, f"Added {random_integer} to the magic list.")
        case _:
            client.publish(to_client, "Unknown request. Try 'menu'.", 0)

print("This runs a stateful broker.")
random.seed()
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"whyhugo")
client.on_connect = on_connect
client.on_message = on_message
#TODO: Use the username and password for your group
client.username_pw_set(config['NTNUpw']['username'], config['NTNUpw']['password'])
client.connect("140.122.185.98", 1883, 60)
client.subscribe(to_server, 0)
client.loop_forever()
