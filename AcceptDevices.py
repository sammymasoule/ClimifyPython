import paho.mqtt.client as mqtt
import requests
import json

# Variables
address = "169.254.12.116:8080"
headers = {'Content-type': 'text/plain'}
MQTT_HOST = "se2-webapp04.compute.dtu.dk"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45


def on_connect(client, userdata, flags, rc):
    client.subscribe("Accept/Devices")


def on_message(client, userdata, msg):
    handle_message(msg)


# Recieve device list request
def handle_message(msg):
    if msg.topic in "Accept/Devices":
        print("Accepting Device")
        # Accept devices rest url

        json_data = json.loads(msg.payload)
        print(json_data['UUID'])

        device_url = "http://" + address + "/rest/inbox/" + json_data['UUID'] + "/approve"
        response = requests.post(device_url)
        print(repr(response.reason))

        if repr(response.reason).__contains__("OK"):
            uuid = json_data['UUID']
            create_data = "{\n" + "\"UniqueID\": " + "\"" + uuid + "\"" "\n}"
            data = json.loads(create_data)
            post_actuator(data)


def post_actuator(data):
    post = requests.post("http://se2-webapp04.compute.dtu.dk/api/api-change-actuator-status.php", data);


# Connection
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Blocking
client.loop_forever()
