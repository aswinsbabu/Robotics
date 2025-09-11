from machine import Pin, time_pulse_us
import board as _board
import time

# Define pins (update according to your wiring)
TRIG_PIN = _board.GP23 #23   # Example GPIO3
ECHO_PIN = _board.GP22 #22   # Example GPIO2

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def get_distance():
    trig.value(0)
    time.sleep_us(2)

    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Wait for echo pulse (timeout ~30ms = 5m)
    duration = time_pulse_us(echo, 1, 30000)

    if duration < 0:
        return None  # no object detected

    # Convert to cm (speed of sound ~34300 cm/s)
    distance_cm = (duration / 2) / 29.1
    return distance_cm

# Main loop
while True:
    dist = get_distance()
    if dist:
        # Use simple string concatenation instead of format
        print("Distance: " + str(round(dist, 2)) + " cm")
    else:
        print("Out of range")
    time.sleep(0.5)
