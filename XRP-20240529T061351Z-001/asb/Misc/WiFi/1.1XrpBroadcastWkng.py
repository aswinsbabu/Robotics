#1.1XrpBroadcastWkng.py==> works with 1.1RPi.py
#Broadcast MAC ID over UDP to the Network 
#     The 1.1 RPi code will capture the IP for the MAC.
from XRPLib.defaults import *

import socket
import network
import time
import ubinascii

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # CRITICAL: Activate first
wlan.connect("Narishimas", "123456798") # Add your credentials

#Wait till WiFi connected
while not wlan.isconnected():
    time.sleep(0.1)

#Read Pico's MAC
mac = ubinascii.hexlify(wlan.config('mac'), ':').decode() 

BCAST_IP = "255.255.255.255"
PORT = 4000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Starting discovery broadcast...")

while True:
    msg = f"PICO_DISCOVERY:{mac}"
    sock.sendto(msg.encode(), (BCAST_IP, PORT)) #send the 'msg'(text+MAC)
    print("Broadcast:", msg)
    time.sleep(2)

''' broadcasts the device's MAC address over UDP so other machines can discover it.
Imports networking and utility modules, then enables the station Wi‑Fi interface and connects to the SSID "Narishimas" with password "123456798".
Waits in a loop until the Wi‑Fi is connected (polling wlan.isconnected()).
Reads the board's MAC with wlan.config('mac') and formats it as a human-readable hex string with colons via ubinascii.hexlify(..., ':').decode().
Creates a UDP socket, enables the SO_BROADCAST option, and repeatedly sends a broadcast packet to 255.255.255.255:4000 every 2 seconds.
Each packet payload is the ASCII string "PICO_DISCOVERY:<MAC>" (e.g., "PICO_DISCOVERY:aa:bb:cc:..."), printed to the console when sent.
  '''
