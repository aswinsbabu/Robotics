from machine import Pin, PWM
import time

# Pin Definitions - Modify if your wiring differs!
# Left Motor
ENC_A_L = Pin(4, Pin.IN)
ENC_B_L = Pin(5, Pin.IN)
PHASE_L = Pin(6, Pin.OUT)
ENABLE_L = PWM(Pin(7))

# Right Motor
ENC_A_R = Pin(12, Pin.IN)
ENC_B_R = Pin(13, Pin.IN)
PHASE_R = Pin(14, Pin.OUT)
ENABLE_R = PWM(Pin(15))

# PWM Frequency
PWM_FREQ = 1000  # 1kHz

# Initialization
ENABLE_L.freq(PWM_FREQ)
ENABLE_R.freq(PWM_FREQ)

# Helper functions for motor control
def set_motor(left_dir, right_dir, speed_l=65535, speed_r=65535):
    """
    Set direction and speed for both motors.

    Args:
        left_dir (int): 1 for forward, 0 for backward (Phase pin logic)
        right_dir (int): 1 for forward, 0 for backward (Phase pin logic)
        speed_l (int): PWM duty (0-65535) for left motor
        speed_r (int): PWM duty (0-65535) for right motor
    """
    PHASE_L.value(left_dir)
    PHASE_R.value(right_dir)
    ENABLE_L.duty_u16(speed_l)
    ENABLE_R.duty_u16(speed_r)

def stop_motors():
    ENABLE_L.duty_u16(0)
    ENABLE_R.duty_u16(0)

# Example movement functions
def move_forward(duration=2, speed=40000):
    # Both motors forward
    set_motor(1, 1, speed, speed)
    time.sleep(duration)
    stop_motors()

def move_backward(duration=2, speed=40000):
    # Both motors backward
    set_motor(0, 0, speed, speed)
    time.sleep(duration)
    stop_motors()

# --- Main Execution Example ---
print("Moving Forward")
move_forward(2, 40000)
time.sleep(1)
print("Moving Backward")
move_backward(2, 40000)
print("Done")
