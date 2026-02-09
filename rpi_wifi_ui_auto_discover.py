import socket
import subprocess
import re

# Hardcoded MAC address
TARGET_MAC = 'XX:XX:XX:XX:XX:XX'  # Replace with the actual MAC address of the XRP robot

def get_ip_address(mac_address):
    print('Scanning for the robot with MAC address:', mac_address)
    # Use arp-scan to find the associated IP address
    try:
        output = subprocess.check_output(['arp-scan', '-l'])
        output = output.decode('utf-8')
        for line in output.split('\n'):
            if mac_address in line:
                ip_address = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
                if ip_address:
                    print('Found IP address:', ip_address[0])
                    return ip_address[0]
    except Exception as e:
        print('Error during scanning:', e)
    return None

if __name__ == '__main__':
    ip = get_ip_address(TARGET_MAC)
    if ip:
        print('Robot IP Address:', ip)
    else:
        print('Robot not found.')