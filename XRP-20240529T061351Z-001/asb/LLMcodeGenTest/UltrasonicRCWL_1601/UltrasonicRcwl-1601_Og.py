from machine import Pin, time_pulse_us
import time

# Define pins (update based on where you connect on XRP board)
TRIG_PIN = 20   # Change Pin no from 3 to 20
ECHO_PIN = 21   # Change Pin no from 2 to 21

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def get_distance():
    # Ensure trig is low
    trig.value(0)
    time.sleep_us(2)

    # Send 10us pulse
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Measure echo pulse duration (timeout = 30ms for ~5m max distance)
    duration = time_pulse_us(echo, 1, 30000)

    if duration < 0:
        return None  # timeout or no object

    # Distance in cm (speed of sound ~34300 cm/s)
    distance_cm = (duration / 2) / 29.1
    return distance_cm

# Main loop
while True:
    dist = get_distance()
    if dist:
        print("Distance: {:.2f} cm".format(dist))
    else:
        print("Out of range")
    time.sleep(0.5)
