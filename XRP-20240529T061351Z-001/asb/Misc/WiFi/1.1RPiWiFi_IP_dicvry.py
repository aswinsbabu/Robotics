#RPi code scanning wifi for Ip of (MAC)known device
import socket
import subprocess
import re
import time

TARGET_MAC = "28:CD:C1:11:5A:C5".lower()
PORT = 4000

def arp_scan(target_mac):
    """Scan ARP table for matching MAC."""
    try:
        result = subprocess.check_output(["arp", "-a"]).decode()
        matches = re.findall(r"\((.*?)\) at ([0-9a-f:]+)", result, re.IGNORECASE)
        for ip, mac in matches:
            if mac.lower() == target_mac:
                return ip
    except:
        pass
    return None

# Setup UDP listener
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # FIX: Added
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # FIX: Added
sock.bind(("", PORT))  # FIX: Changed from "0.0.0.0" to ""
sock.settimeout(1)

print("Listening for Pico W...")

while True:
    try:
        data, (ip, _) = sock.recvfrom(1024)
        data = data.decode()
        if "PICO_DISCOVERY:" in data:
            # FIX: Correct MAC parsing
            parts = data.split(":", 1)
            if len(parts) == 2:
                mac = parts[1].strip().lower()
                if mac == TARGET_MAC:
                    print("Found Pico W via broadcast:", ip)
                    break
    except socket.timeout:
        pass

    # Fallback to ARP scan
    ip = arp_scan(TARGET_MAC)
    if ip:
        print("Found Pico W via ARP:", ip)
        break

    print("Not found yet, retrying...")
    time.sleep(1)
