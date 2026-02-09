"""
File 1.0_Wifi_Close_BtnOnTile.py
Parent:1.42_CloseButtonOnTiles.py(XRP-20240529T061351Z-001/asb/KidsProgramUI/RPIbased/latest/1.42_)
import subprocess
import re
XRP Robot WiFi Receiver Code
Connects to WiFi and receives commands via UDP socket
Replaces USB serial communication
"""

from XRPLib.defaults import *
import socket
import time
import threading
import sys

# WiFi Configuration
WIFI_SSID = 'Narishimas'
WIFI_PASSWORD = '123456798'
ROBOT_UDP_PORT = 5005  # Port the robot listens on
BUFFER_SIZE = 1024

# Socket for receiving commands
robot_socket = None

def setup_wifi():
    """Connect robot to WiFi network"""
    print("Connecting to WiFi...")
    try:
        # This assumes XRP has WiFi connectivity (MicroPython compatible)
        # For RoboRIO or similar platforms, adjust accordingly
        import network
        
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        
        if not wlan.isconnected():
            print(f"Connecting to {WIFI_SSID}...")
            wlan.connect(WIFI_SSID, WIFI_PASSWORD)
            
            # Wait for connection
            timeout = 20  # 20 seconds timeout
            while not wlan.isconnected() and timeout > 0:
                time.sleep(0.5)
                timeout -= 1
        
        if wlan.isconnected():
            print("✓ WiFi Connected!")
            print(f"IP Address: {wlan.ifconfig()[0]}")
            return True
        else:
            print("✗ WiFi Connection Failed")
            return False
            
    except Exception as e:
        print(f"WiFi Error: {e}")
        return False

def setup_socket():
    """Setup UDP socket to receive commands"""
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        robot_socket.bind(('0.0.0.0', ROBOT_UDP_PORT))
        robot_socket.settimeout(0.1)  # Non-blocking with short timeout
        print(f"✓ UDP Socket listening on port {ROBOT_UDP_PORT}")
        return True
    except Exception as e:
        print(f"Socket Error: {e}")
        return False

def execute_command(command):
    """Execute movement commands with proper timing"""
    drive_time = 1.0
    try:
        command = command.strip().lower()
        
        if command == 'forward':
            print("→ FORWARD")
            drivetrain.set_effort(0.8, 0.8)
            time.sleep(drive_time)
            drivetrain.stop()
            
        elif command == 'backward':
            print("← BACKWARD")
            drivetrain.set_effort(-0.8, -0.8)
            time.sleep(drive_time)
            drivetrain.stop()
            
        elif command == 'left':
            print("↖ LEFT")
            drivetrain.set_effort(-0.8, 0.8)
            time.sleep(drive_time)
            drivetrain.stop()
            
        elif command == 'right':
            print("↗ RIGHT")
            drivetrain.set_effort(0.8, -0.8)
            time.sleep(drive_time)
            drivetrain.stop()
            
        elif command == 'stop':
            print("⏹ STOP")
            drivetrain.set_effort(0, 0)
            time.sleep(0.2)
            drivetrain.stop()
            
        else:
            print(f"⚠ Unknown command: {command}")
            
    except Exception as e:
        print(f"Command Error: {e}")
    finally:
        drivetrain.set_effort(0, 0)  # Ensure stop after each command

def receive_commands():
    """Continuously listen for incoming WiFi commands"""
    print("\n🤖 XRP Robot Ready! Listening for WiFi commands...\n")
    
    while True:
        try:
            if robot_socket:
                data, addr = robot_socket.recvfrom(BUFFER_SIZE)
                command = data.decode('utf-8')
                print(f"📡 Command received from {addr[0]}: {command}")
                execute_command(command)
                
        except socket.timeout:
            # Normal timeout, continue listening
            time.sleep(0.01)
        except Exception as e:
            print(f"Receive Error: {e}")
            time.sleep(0.1)

def main():
    """Initialize robot and start listening"""
    print("="*50)
    print("XRP ROBOT - WiFi Receiver")
    print("="*50)
    
    # Setup WiFi
    if not setup_wifi():
        print("Failed to connect to WiFi. Check network credentials.")
        return
    
    # Setup Socket
    if not setup_socket():
        print("Failed to setup socket.")
        return
    
    # Start receiving commands
    try:
        receive_commands()
    except KeyboardInterrupt:
        print("\n\nRobot shutting down...")
        if robot_socket:
            robot_socket.close()
        drivetrain.stop()

if __name__ == '__main__':
    main()
