import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print(f"Connect failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}' with QoS {msg.qos}")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_start()

topic = "taipeiMetro/station/entrance"
client.subscribe(topic, qos=0)

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")

client.loop_stop()

client.disconnect()
