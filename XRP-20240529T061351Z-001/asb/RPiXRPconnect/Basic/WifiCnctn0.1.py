from XRPLib.defaults import *
import network
import time

# Create a WLAN object
wlan = network.WLAN(network.STA_IF)

# Activate the network interface
wlan.active(True)

# Connect to the Wi - Fi network
wlan.connect('Narishimas', '123456798')

# Wait for the connection

while not wlan.isconnected():
    time.sleep(1)

#while(1):
print('Connected to Wi - Fi:', wlan.ifconfig())


