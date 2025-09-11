from machine import Pin, time_pulse_us
import time

# XRP Beta pinout (from SparkFun docs):
TRIG_PIN = 22   # GPIO20 = Range Trigger
ECHO_PIN = 28   # GPIO21 = Range Echo

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def get_distance_cm():
    trig.value(0)
    time.sleep_us(2)

    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duration = time_pulse_us(echo, 1, 30000)  # wait for echo, 30ms timeout

    if duration < 0:
        return None  # no response

    return (duration / 2) / 29.1  # convert to cm

while True:
    dist = get_distance_cm()
    if dist is None:
        print("Out of range")
    else:
        # Avoid Unicode/formatting -> just cast to int
        #print("Distance:", int(dist), "cm")
        print("Distance (cm):", round(dist,2))
    time.sleep(0.5)
