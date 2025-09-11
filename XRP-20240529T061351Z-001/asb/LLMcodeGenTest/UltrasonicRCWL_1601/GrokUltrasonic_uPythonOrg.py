import machine
import time

# Pin definitions
TRIG_PIN = 20
ECHO_PIN = 21
LEFT_MOTOR_PIN = 0  # PWM for left motor
RIGHT_MOTOR_PIN = 1  # PWM for right motor

# Initialize pins
trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)
left_motor = machine.PWM(machine.Pin(LEFT_MOTOR_PIN))
right_motor = machine.PWM(machine.Pin(RIGHT_MOTOR_PIN))

# Set PWM frequency (1kHz typical for motors)
left_motor.freq(1000)
right_motor.freq(1000)

# Constants
SPEED_OF_SOUND = 343  # m/s
DISTANCE_THRESHOLD = 0.5  # meters
FORWARD_SPEED = 512  # PWM duty cycle (0-1023, half speed ~512)
STOP_SPEED = 0

def get_distance():
    # Send 10us trigger pulse
    trig.value(0)
    time.sleep_us(2)  # 2us low
    trig.value(1)
    time.sleep_us(10)  # 10us high
    trig.value(0)
    
    # Measure echo pulse duration
    start_time = time.ticks_us()
    timeout = start_time + 100000  # 100ms timeout in microseconds
    
    # Wait for echo to go high
    while not echo.value() and time.ticks_diff(time.ticks_us(), start_time) < time.ticks_diff(timeout, start_time):
        pass
    pulse_start = time.ticks_us()
    
    # Wait for echo to go low
    while echo.value() and time.ticks_diff(time.ticks_us(), pulse_start) < time.ticks_diff(timeout, pulse_start):
        pass
    pulse_end = time.ticks_us()
    
    # Calculate pulse duration and distance
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    distance = (pulse_duration * SPEED_OF_SOUND) / (2 * 1000000)  # Convert us to seconds, then to meters
    
    # Return -1 if out of range (2cm-450cm for RCWL-1601)
    if 0.02 <= distance <= 4.5:
        return distance
    else:
        return -1

# Main loop
while True:
    distance = get_distance()
    
    # Print distance for debugging (view via serial monitor, e.g., Thonny or screen)
    if distance >= 0:
        print(f"Distance: {distance:.2f}m")
    else:
        print("Distance: Out of range")
    
    # Simple obstacle avoidance
    if distance >= 0 and distance < DISTANCE_THRESHOLD:
        left_motor.duty_u16(STOP_SPEED)
        right_motor.duty_u16(STOP_SPEED)
        print("Obstacle detected - Stopping")
    else:
        left_motor.duty_u16(FORWARD_SPEED)
        right_motor.duty_u16(FORWARD_SPEED)
        print("Moving forward")
    
    time.sleep(0.1)  # 100ms loop delay