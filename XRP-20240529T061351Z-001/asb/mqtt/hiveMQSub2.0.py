# Subscribed to a topic
# Working code for Mqtt connection
# HIVEmq
import network
from umqtt.simple import MQTTClient
import time
import machine
import ssl

MQTT_BROKER = "5c4849f0caf34edf9bce57b8bc3f7ff2.s1.eu.hivemq.cloud"
MQTT_PORT = 0
MQTT_CLIENT_ID = "PICO"
MQTT_USER = "asbxrp"
MQTT_PASSWORD = "Digikey@2024"

# Connect to the WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Asb wifi", "123456798")

while not wlan.isconnected():
    time.sleep(1)
    
print("Connected to the WiFi")

# Callback function to handle incoming messages
def subcptn_CallBack(sub_topic, msg):
    print("Received message:", msg, "on topic:", sub_topic)
    if sub_topic == b'xrp/msg':
        print('Message on xrp/msg topic:', msg)

# HiveMQ
pub_topic_temp = "topic/temp"
sub_topic = "xrp/msg"
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_NONE

# MQTT credentials
mqtt_client = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, ssl=context)
mqtt_client.set_callback(subcptn_CallBack)  # Set callback function
mqtt_client.connect()  # Connecting 

print("Connected to HiveMQ broker")

mqtt_client.subscribe(sub_topic)  # Subscribe to the topic
print('Connected to %s MQTT broker, subscribed to %s topic' % (MQTT_BROKER, sub_topic))

# Start listening for messages
while True:
    mqtt_client.wait_msg()  # Wait for a message to arrive
