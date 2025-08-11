from machine import Pin, PWM
import time

# Define motor control pins
# Left Motor
left_phase = Pin(6, Pin.OUT)
left_enable = PWM(Pin(7))
left_enable.freq(1000)  # Set PWM frequency to 1kHz #PWM(Pin(7)).freq(1000)

# Right Motor
right_phase = Pin(14, Pin.OUT)
right_enable = PWM(Pin(15))
right_enable.freq(1000)  # Set PWM frequency to 1kHz

# Function to move forward
def move_forward(speed=50000, duration=2):
    
    # Set direction: forward
    left_phase.value(1)
    right_phase.value(0)
    
    # Set speed
    left_enable.duty_u16(speed)
    right_enable.duty_u16(speed)
    
    # Move for specified duration
    time.sleep(duration)
    # Stop motors
    left_enable.duty_u16(0)
    right_enable.duty_u16(0)

# Function to move backward
def move_backward(speed=50000, duration=2):
    # Set direction: backward
    left_phase.value(0)
    right_phase.value(1)
    
    # Set speed
    left_enable.duty_u16(speed)
    right_enable.duty_u16(speed)
    
    # Move for specified duration
    time.sleep(duration)
    
    # Stop motors
    left_enable.duty_u16(0)
    right_enable.duty_u16(0)

# Main loop

move_forward()
time.sleep(1)
move_backward()
time.sleep(1)
