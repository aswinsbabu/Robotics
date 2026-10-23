#USB device scanner on Ubuntu and RPI python
#!/usr/bin/env python3

import serial.tools.list_ports


def scan_usb_serial_devices():
    """List available serial ports and their reported device details."""

    ports = serial.tools.list_ports.comports()
    devices_found = []

    if not ports:
        print("No serial ports detected.")
        return devices_found

    print("Serial devices detected:\n")

    for port in ports:
        device_info = {
            "device": port.device,
            "name": port.name,
            "description": port.description,
            "manufacturer": port.manufacturer,
            "product": port.product,
            "serial_number": port.serial_number,
            "vid": port.vid,
            "pid": port.pid,
            "hwid": port.hwid,
        }

        devices_found.append(device_info)

        print(f"Device path  : {port.device}")
        print(f"Port name    : {port.name}")
        print(f"Description  : {port.description}")
        print(f"Manufacturer : {port.manufacturer}")
        print(f"Product      : {port.product}")
        print(f"Serial number: {port.serial_number}")
        print(f"Vendor ID    : {port.vid}")
        print(f"Product ID   : {port.pid}")
        print(f"Hardware ID  : {port.hwid}")
        print("-" * 40)

    return devices_found


if __name__ == "__main__":
    detected_devices = scan_usb_serial_devices()
    print(f"\nTotal serial ports detected: {len(detected_devices)}")
