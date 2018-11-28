import paho.mqtt.client as mqtt
import requests

# Variables
address = "169.254.12.116:8080"
headers = {'Content-type': 'text/plain'}
MQTT_HOST = "se2-webapp04.compute.dtu.dk"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_SUB_TOPIC = "Accept/Devices"
MQTT_SUB_TOPIC = "Disconnect/Devices"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe(MQTT_SUB_TOPIC)


def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    handle_message(msg)


# Recieve device list request
def handle_message(msg):
    if msg.topic in "Accept/Devices":
        print("Accepting Device")
        # Accept devices rest url
        print(repr(msg.payload))
        thingUID = repr(msg.payload)
        device_url = "http://" + address + "/rest//inbox/" + thingUID[0] + "/approve"
        response = requests.post(device_url, thingUID[1])
        print(repr(response))

    if msg.topic in "Disconnect/Devices":
        print("Disconnect Device")
        # Temperature rest url
        print(repr(msg.payload))
        thingUID = repr(msg.payload)
        device_url = "http://" + address + "/rest//inbox/" + thingUID[0]
        response = requests.delete(device_url, thingUID[0])
        print(repr(response))


# Connection
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Blocking
client.loop_forever()
