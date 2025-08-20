import socket
import subprocess
import os
import time

# -------------------------------
# Step 1: Configure Access Point
# -------------------------------

# Define AP credentials
SSID = "Narishimas"
PASSWORD = "123456798"

# Paths for temporary config files
HOSTAPD_CONF = "/tmp/hostapd.conf"
DNSMASQ_CONF = "/tmp/dnsmasq.conf"

# Write hostapd configuration
with open(HOSTAPD_CONF, "w") as f:
    f.write(f"""
interface=wlan0
driver=nl80211
ssid={SSID}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={PASSWORD}
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
    """.strip())

# Write dnsmasq configuration
with open(DNSMASQ_CONF, "w") as f:
    f.write("""
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
    """.strip())

# Set static IP for wlan0
subprocess.run(["ip", "link", "set", "wlan0", "down"])
subprocess.run(["ip", "addr", "add", "192.168.4.1/24", "dev", "wlan0"])
subprocess.run(["ip", "link", "set", "wlan0", "up"])

# Start dnsmasq with custom config
subprocess.Popen(["dnsmasq", "--no-daemon", "--conf-file=" + DNSMASQ_CONF],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Start hostapd with custom config
subprocess.Popen(["hostapd", HOSTAPD_CONF],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Wait a few seconds for AP to initialize
print("Setting up Access Point...")
time.sleep(5)
print(f"Access Point '{SSID}' is now active.")

# -------------------------------
# Step 2: Start TCP Server
# -------------------------------

HOST = ''       # Listen on all interfaces (including wlan0)
PORT = 12345    # TCP port to listen on

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen(1)
print(f"TCP Server listening on port {PORT}...")

# Accept a client connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Handle client communication
while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print("Received from client:", data)
    conn.send(f"ACK: {data}".encode())

# Close the connection
conn.close()
print("Connection closed.")
