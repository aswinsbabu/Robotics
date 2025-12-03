#Broadcast MAC
from XRPLib.defaults import *

import socket
import network
import time
import ubinascii

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # CRITICAL: Activate first
wlan.connect("Narishimas", "123456798") # Add your credentials
while not wlan.isconnected():
    time.sleep(0.1)

mac = ubinascii.hexlify(wlan.config('mac'), ':').decode()

BCAST_IP = "255.255.255.255"
PORT = 4000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Starting discovery broadcast...")

while True:
    msg = f"PICO_DISCOVERY:{mac}"
    sock.sendto(msg.encode(), (BCAST_IP, PORT))
    print("Broadcast:", msg)
    time.sleep(2)
