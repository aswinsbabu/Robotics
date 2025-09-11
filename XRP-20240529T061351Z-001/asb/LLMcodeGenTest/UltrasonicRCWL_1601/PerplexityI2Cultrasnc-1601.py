from machine import Pin, I2C
import time

# Use I2C0 pins. Adjust numbers based on actual XRP board wiring.
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=100000)  # Example pins, adapt to XRP header

RCWL1601_ADDR = 0x57

def read_distance():
    # Start ranging (write '1')
    i2c.writeto(RCWL1601_ADDR, b'\x01')
    time.sleep_ms(60)  # Wait for measurement
    # Read 3 bytes
    data = i2c.readfrom(RCWL1601_ADDR, 3)
    distance_um = data << 16 | data[1] << 8 | data[2]
    distance_mm = distance_um // 1000
    return distance_mm

while True:
    try:
        d = read_distance()
        print("Distance: {} mm".format(d))
    except Exception as e:
        print("Error reading sensor:", e)
    time.sleep(0.5)
