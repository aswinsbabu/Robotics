# micropython_ble_hello.py
# This script runs on Raspberry Pi Pico W using MicroPython.
# It creates a BLE peripheral that advertises a service and sends "Hello World" repeatedly.

import bluetooth
import time

# Initialize the Bluetooth Low Energy (BLE) interface
ble = bluetooth.BLE()
ble.active(True)  # Activate BLE

# Define custom UUIDs for the service and characteristic
SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
CHAR_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")

# Register the service and characteristic with the BLE stack
# gatts_register_services returns a tuple of handles for the service and its characteristics
service = ble.gatts_register_services([(SERVICE_UUID, (CHAR_UUID,))])
handle = service[0][1][0]  # Get the handle for the characteristic

# Start advertising the BLE device so it can be discovered
# The advertising payload includes flags and a short name ("HelloPico")
ble.gap_advertise(100, b'\x02\x01\x06\x03\x03\xf0\xab\x0fHelloPico')

print("Advertising BLE service...")

# Main loop: write "Hello World" to the characteristic every 2 seconds
while True:
    ble.gatts_write(handle, b"Hello World")  # Update characteristic value
    print("Sent: Hello World")  # Debug print
    time.sleep(2)  # Wait before sending again
