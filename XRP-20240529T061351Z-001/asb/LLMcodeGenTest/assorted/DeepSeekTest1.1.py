from machine import Pin, PWM
import time

# Motor Pin Definitions (DRV8835)
# Left Motor
LEFT_PHASE = Pin(6, Pin.OUT)    # GPIO6 - Phase pin (direction)
LEFT_ENABLE = PWM(Pin(7))       # GPIO7 - Enable pin (speed)
LEFT_ENABLE.freq(1000)          # PWM frequency: 1kHz

# Right Motor
RIGHT_PHASE = Pin(14, Pin.OUT)  # GPIO14 - Phase pin (direction)
RIGHT_ENABLE = PWM(Pin(15))      # GPIO15 - Enable pin (speed)
RIGHT_ENABLE.freq(1000)         # PWM frequency: 1kHz

# Encoder Pins (Not used here, but defined for future use)
LEFT_ENCODER_A = Pin(4, Pin.IN)   # GPIO4 - Left Encoder A
LEFT_ENCODER_B = Pin(5, Pin.IN)   # GPIO5 - Left Encoder B
RIGHT_ENCODER_A = Pin(12, Pin.IN) # GPIO12 - Right Encoder A
RIGHT_ENCODER_B = Pin(13, Pin.IN) # GPIO13 - Right Encoder B

def set_motor_speed(motor_phase, motor_enable, speed):
    """Control motor direction and speed.
    Args:
        motor_phase: Phase pin (direction)
        motor_enable: Enable pin (PWM speed)
        speed: -1.0 (full reverse) to 1.0 (full forward)
    """
    if speed > 0:
        motor_phase.value(1)  # Forward
    else:
        motor_phase.value(0)  # Backward
    motor_enable.duty_u16(int(abs(speed) * 65535))  # 16-bit PWM (0-65535)

def move_forward(speed=0.5):
    """Move robot forward at given speed (0.0 to 1.0)."""
    set_motor_speed(LEFT_PHASE, LEFT_ENABLE, speed)
    set_motor_speed(RIGHT_PHASE, RIGHT_ENABLE, -speed)

def move_backward(speed=0.5):
    """Move robot backward at given speed (0.0 to 1.0)."""
    set_motor_speed(LEFT_PHASE, LEFT_ENABLE, -speed)
    set_motor_speed(RIGHT_PHASE, RIGHT_ENABLE, speed)

def stop():
    """Stop both motors."""
    LEFT_ENABLE.duty_u16(0)
    RIGHT_ENABLE.duty_u16(0)

# Main loop
#while True:
print("Moving Forward")
move_forward(0.5)  # 50% speed
time.sleep(2)

print("Stopping")
stop()
time.sleep(1)

print("Moving Backward")
move_backward(0.5)  # 50% speed
time.sleep(2)

print("Stopping")
stop()
time.sleep(1)