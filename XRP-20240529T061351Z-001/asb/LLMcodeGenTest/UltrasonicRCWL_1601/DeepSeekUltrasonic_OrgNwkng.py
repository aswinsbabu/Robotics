#!/usr/bin/env python3
"""
XRP Robot with RCWL-1601 Ultrasonic Sensor Interface
Measures distance and responds to obstacles
"""

import time
from xrp import *
from XRPLib import board #import board
#import digitalio

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        """Initialize the ultrasonic sensor"""
        # Set up trigger pin as output
        self.trig = digitalio.DigitalInOut(trig_pin)
        self.trig.direction = digitalio.Direction.OUTPUT
        
        # Set up echo pin as input
        self.echo = digitalio.DigitalInOut(echo_pin)
        self.echo.direction = digitalio.Direction.INPUT
        
        # Speed of sound in cm/s
        self.speed_of_sound = 34300  # cm/s
        
    def get_distance(self):
        """Get distance measurement in centimeters"""
        # Ensure trigger is low initially
        self.trig.value = False
        time.sleep(0.0001)  # 100us delay
        
        # Send 10us pulse to trigger
        self.trig.value = True
        time.sleep(0.00001)  # 10us
        self.trig.value = False
        
        # Wait for echo to go high
        timeout = time.time() + 0.1  # 100ms timeout
        while not self.echo.value:
            if time.time() > timeout:
                return -1  # Timeout error
        
        # Measure pulse duration
        pulse_start = time.time()
        timeout = time.time() + 0.1  # 100ms timeout
        while self.echo.value:
            if time.time() > timeout:
                return -1  # Timeout error
        
        pulse_end = time.time()
        
        # Calculate distance
        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * self.speed_of_sound) / 2
        
        return distance

def main():
    """Main program function"""
    print("XRP Robot with Ultrasonic Sensor - Starting...")
    
    # Initialize XRP components
    #robot = XRP()
    led = robot.led
    buzzer = robot.buzzer
    
    # Initialize ultrasonic sensor
    ultrasonic = UltrasonicSensor(board.D0, board.D1)  # D0=TRIG, D1=ECHO
    
    # Safe distance threshold (in cm)
    SAFE_DISTANCE = 20.0
    
    try:
        while True:
            # Get distance measurement
            distance = ultrasonic.get_distance()
            
            if distance == -1:
                print("Measurement error or timeout")
                led.set_all(255, 0, 0)  # Red LED for error
            else:
                print(f"Distance: {distance:.2f} cm")
                
                # React based on distance
                if distance < SAFE_DISTANCE:
                    # Object too close - stop and alert
                    robot.drive(0, 0)  # Stop moving
                    led.set_all(255, 0, 0)  # Red LED
                    buzzer.beep(0.2)  # Short beep
                    print("Obstacle detected! Stopping.")
                else:
                    # Clear path - continue moving
                    robot.drive(0.3, 0)  # Move forward slowly
                    led.set_all(0, 255, 0)  # Green LED
                    print("Path clear. Moving forward.")
            
            # Wait before next measurement
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    finally:
        # Clean up
        robot.drive(0, 0)  # Stop motors
        led.off()  # Turn off LED
        print("Robot stopped and cleaned up")

# Advanced version with obstacle avoidance
def obstacle_avoidance_demo():
    """Advanced obstacle avoidance demonstration"""
    print("Starting Obstacle Avoidance Demo...")
    
    robot = XRP()
    ultrasonic = UltrasonicSensor(board.D0, board.D1)
    
    try:
        while True:
            distance = ultrasonic.get_distance()
            
            if distance != -1:
                print(f"Distance: {distance:.2f} cm")
                
                if distance < 15:  # Very close
                    # Back up and turn
                    robot.drive(-0.2, 0)  # Reverse
                    time.sleep(0.5)
                    robot.drive(0, 0.5)  # Turn right
                    time.sleep(0.8)
                elif distance < 30:  # Moderately close
                    # Slow down and prepare to turn
                    robot.drive(0.1, 0.2)  # Slow forward with slight turn
                else:
                    # Clear path - normal speed
                    robot.drive(0.4, 0)  # Forward
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Demo stopped")
    finally:
        robot.drive(0, 0)

if __name__ == "__main__":
    # Run the main program
    main()
    
    # Uncomment the line below to run the advanced demo instead
    # obstacle_avoidance_demo()
    