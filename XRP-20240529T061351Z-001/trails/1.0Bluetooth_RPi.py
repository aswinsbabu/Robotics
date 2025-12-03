# python_ble_client.py
# This script runs on Raspberry Pi using standard Python.
# It connects to the Pico W via BLE and reads the "Hello World" message repeatedly.

import asyncio
from bleak import BleakClient, BleakScanner

# UUIDs must match those defined in the MicroPython script
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

async def main():
    print("Scanning for Pico W...")
    # Discover nearby BLE devices
    devices = await BleakScanner.discover()
    pico_device = None

    # Look for the device advertising with name "HelloPico"
    for d in devices:
        if "HelloPico" in d.name:
            pico_device = d
            break

    if not pico_device:
        print("Pico W not found!")
        return

    print(f"Connecting to {pico_device.address}...")
    # Connect to the Pico W using its BLE address
    async with BleakClient(pico_device.address) as client:
        print("Connected!")
        # Continuously read the characteristic value every 2 seconds
        while True:
            data = await client.read_gatt_char(CHAR_UUID)  # Read from characteristic
            print(f"Received: {data.decode()}")  # Decode bytes to string
            await asyncio.sleep(2)  # Wait before reading again

# Run the async main function
asyncio.run(main())
