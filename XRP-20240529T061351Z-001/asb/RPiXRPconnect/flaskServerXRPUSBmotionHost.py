#Pico XRP side code
from XRPLib.defaults import *
import time
import sys
import machine

def corr_Motion(command):
    if command == 'F':  # Forward command
        drivetrain.set_effort(0.5, 0.5)
        time.sleep(2)
        
        drivetrain.set_effort(0, 0) #Stop the robot
        time.sleep(1) #wait for some 1 sec 
    elif command == 'B':  # Backward command
        drivetrain.set_effort(-0.5, -0.5)
        time.sleep(2) #wait for some time
        
        drivetrain.set_effort(0, 0) #Stop the robot
        time.sleep(1) #wait for some 1 sec
    elif command == 'L':  # Left command
        drivetrain.set_effort(-0.5, 0.5)
        time.sleep(2)
        drivetrain.set_effort(0, 0) #Stop the robot
        time.sleep(1) #wait for some 1 sec
    elif command == 'R':  # Right command
        drivetrain.set_effort(0.5, -0.5)
        time.sleep(2)
        
        drivetrain.set_effort(0, 0) #Stop the robot
        time.sleep(1) #wait for some 1 sec
    else:
        drivetrain.set_effort(0, 0)  # Stop if unknown command
        time.sleep(5) #wait for some 5 sec
    return None
while True:
    # read a command from the host
    #serialMsg= sys.stdin.readline().strip()
    serialMsg= sys.stdin.readline().strip()
    print('Serial Message: ', serialMsg)
    corr_Motion(serialMsg)
