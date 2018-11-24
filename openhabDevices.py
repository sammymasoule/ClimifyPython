import json
import paho.mqtt.client as mqtt
import requests

# Variables
address = "169.254.12.116:8080"
headers = {'Content-type': 'text/plain'}
MQTT_HOST = "se2-webapp04.compute.dtu.dk"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_SUB_TOPIC = "Get/Devices"
MQTT_PUB_TOPIC = "Send/Devices"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe(MQTT_SUB_TOPIC)


def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))

    # Discover things on z-wave binding
    print("Start zwave discovery")
    search_url = "http://" + address + "/rest/discovery/bindings/zwave/scan"
    searchresp = requests.post(search_url)
    print(repr(searchresp))

    handle_message(msg)


# Recieve device list request
def handle_message(msg):
        if msg.topic in "Get/Devices":
            print("Fetching inbox data")
            # Temperature rest url
            device_url = "http://" + address + "/rest/inbox"

            # Creating request for devices
            response = requests.get(device_url, headers=headers)
            print(repr(response))
            tempvar = json.loads(response.content)

            tmplabel = tempvar[0]['label']
            label = tmplabel.replace(':', '¥')

            tmpgenericclass = tempvar[0]['properties']['zwave_class_generic']
            genericclass = tmpgenericclass.replace(':', '¥')

            tmpthinguid = tempvar[0]['thingUID']
            thinguid = tmpthinguid.replace(':', '¥')

            create_data = "{\n" + "\"label\": " + "\"" + label + "\"" + ",\n" + \
                          "\"zwave_class_generic\": " + "\"" + genericclass + "\"" + ",\n" + \
                          "\"thingUID\": " + "\"" + thinguid + "\"" + "\n}"

            data = json.loads(create_data)
            print(data)
            send_message(create_data)
            post_actuator(data)


# Send device list
def send_message(MQTT_MSG):
    client.publish(MQTT_PUB_TOPIC, MQTT_MSG)


# Insert data into mySQL on SE2-vm
def post_actuator(data):
    post = requests.post("http://se2-webapp04.compute.dtu.dk/api/api-post-actuators.php", data);


# Connection
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Blocking
client.loop_forever()
