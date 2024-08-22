import network
from umqtt.simple import MQTTClient
import time
import machine
import ssl

MQTT_BROKER="5c4849f0caf34edf9bce57b8bc3f7ff2.s1.eu.hivemq.cloud"
MQTT_PORT=0
MQTT_CLIENT_ID="PICO"
MQTT_USER="asbxrp"
MQTT_PASSWORD="Digikey@2024"

#connect to the WiFi

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Asb wifi", "123456798")

while not wlan.isconnected():
    time.sleep(1)
    
print("Connected to the WiFi")
    
#HiveMQ

pub_topic_temp="topic/temp"

context = ssl.SSLContext (ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_NONE

mqtt_client = MQTTClient(client_id= MQTT_CLIENT_ID, server = MQTT_BROKER, port = MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, ssl = context)

mqtt_client.connect();

print("Connected to HiveMQ broker")
