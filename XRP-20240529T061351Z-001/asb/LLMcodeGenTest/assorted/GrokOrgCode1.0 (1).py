import machine
import time

# Define GPIO pins for Left Motor
LEFT_EN_PIN = 7  # Enable Pin
LEFT_PHASE_PIN = 6  # Phase Pin
LEFT_ENCODER_A_PIN = 4  # Encoder A Pin
LEFT_ENCODER_B_PIN = 5  # Encoder B Pin

# Define GPIO pins for Right Motor
RIGHT_EN_PIN = 15  # Enable Pin
RIGHT_PHASE_PIN = 14  # Phase Pin
RIGHT_ENCODER_A_PIN = 12  # Encoder A Pin
RIGHT_ENCODER_B_PIN = 13  # Encoder B Pin

# Set up Pins
left_en = machine.Pin(LEFT_EN_PIN, machine.Pin.OUT)
left_phase = machine.Pin(LEFT_PHASE_PIN, machine.Pin.OUT)

right_en = machine.Pin(RIGHT_EN_PIN, machine.Pin.OUT)
right_phase = machine.Pin(RIGHT_PHASE_PIN, machine.Pin.OUT)

def init_motors():
    # Initially stop both motors
    left_en.value(0)
    right_en.value(0)

def move_forward():
    print("Moving forward")
    left_en.value(1)
    left_phase.value(1)  # Set left motor to forward
    right_en.value(1)
    right_phase.value(1)  # Set right motor to forward
    
def move_backward():
    print("Moving backward")
    left_en.value(1)
    left_phase.value(0)  # Set left motor to backward
    right_en.value(1)
    right_phase.value(0)  # Set right motor to backward

def stop_motors():
    print("Stopping motors")
    left_en.value(0)
    right_en.value(0)

# Main loop to drive the motors
try:
    init_motors()  # Initialize motors

    while True:
        move_forward()  # Move forward
        time.sleep(2)  # Move forward for 2 seconds
        
        stop_motors()  # Stop motors
        time.sleep(1)  # Wait for 1 second
        
        move_backward()  # Move backward
        time.sleep(2)  # Move backward for 2 seconds
        
        stop_motors()  # Stop motors
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    stop_motors()  # Stop motors on keyboard interrupt
    print("Program stopped.")
    
    