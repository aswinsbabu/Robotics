#Simple Wifi Data transfer(helloworld)
#XRP side code
from XRPLib.defaults import *

import network
import socket
import time

SSID = 'Narishimas'
PASSWORD = '123456798'

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
print("Connecting to Wi-Fi...", end="")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(1)
print("\nConnected. IP:", wlan.ifconfig()[0])

# Create TCP socket server
addr = socket.getaddrinfo('0.0.0.0', 12345)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Listening on", addr)

while True:
    cl, client_addr = s.accept()
    print("Client connected from", client_addr)
    data = cl.recv(1024)
    if data:
        msg = data.decode().strip()
        print("Received:", msg)
        # Optionally reply:
        cl.send(b"ack\n")
    cl.close()
