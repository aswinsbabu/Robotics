from machine import Pin, time_pulse_us
from utime import sleep

# Choose two GPIO pins for Trig and Echo (adjust for XRP wiring)
TRIG_PIN = 3    # example GPIO number (Use XRP-specific assignment)
ECHO_PIN = 2    # example GPIO number (Use XRP-specific assignment)

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def measure_distance_cm():
    trig.low()
    sleep(0.01)      # 10 ms settle

    # Send trigger pulse
    trig.high()
    sleep_us(10)
    trig.low()

    # Measure echo response time
    duration = time_pulse_us(echo, 1, 100000)    # Max wait: 100 ms
    if duration < 0:
        return None   # Timeout or error

    # Calculate distance (Half round-trip for ultrasonic pulse)
    distance_cm = (duration * 0.0343) / 2
    return distance_cm

while True:
    distance = measure_distance_cm()
    if distance is None:
        print("Out of range or error!")
    else:
        print("Distance: {:.2f} cm".format(distance))
    sleep(1)
