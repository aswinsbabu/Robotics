#File:1.0PredatorModeToAndFro.py
#Parent:Sensor_examples.py; https://github.com/Open-STEM/XRP_MicroPython/blob/main/XRPExamples/sensor_examples.py
#Like a lion standoff
#Approach if ultrasonic distance is too much and fall back if too close

from XRPLib.defaults import *
import time

"""
    By the end of this file students will learn how to read and use data from
    both the ultrasonic sensors and the line followers.
    They will also have a chance to learn the basics of proportional control.
"""

# Polling data from the ultrasonic sensor
def ultrasonic_test():
    while True:
        print(rangefinder.distance())
        time.sleep(0.1)

# Approaches a wall at a set speed and then stops
def drive_till_close(target_distance: float = 15.0):
    move_back_distance=8.0
    speed = 0.6
    while(1):
        print(rangefinder.distance())
        print("target_distance=",target_distance)
        if rangefinder.distance() > target_distance:#move forward if obstacle is far
            drivetrain.set_effort(speed, speed)
            time.sleep(0.1)
        elif rangefinder.distance() < move_back_distance: #move backward if obstacle is too close
            drivetrain.set_effort(-0.6, -0.6)
            time.sleep(0.1)
        elif rangefinder.distance() < target_distance: #Stop if obstacle is at the target distance
            drivetrain.set_effort(0, 0)
            time.sleep(0.1)
        


#ultrasonic_test()
drive_till_close()

