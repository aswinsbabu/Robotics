#Only display the   Device port name for XRP serial number

#!/usr/bin/env python3

import serial.tools.list_ports

TARGET_SERIAL_NUMBER = "e66178758b81ab31"


def scan_usb_serial_devices():
    """Print the device path of the USB serial device matching the target serial number."""

    ports = serial.tools.list_ports.comports()

    for port in ports:
        if port.serial_number == TARGET_SERIAL_NUMBER:
            print(port.device)
            return port.device

    # No matching device found
    return None


if __name__ == "__main__":
    device_path = scan_usb_serial_devices()

    if device_path is None:
        print("Device not found.", file=__import__("sys").stderr)

