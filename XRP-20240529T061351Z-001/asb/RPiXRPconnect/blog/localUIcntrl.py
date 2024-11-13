# Filename: xrp_motion_cntrl.py
# Author: Aswin S Babu
# Description: This script controls the movement of an XRP robot based on commands received through a serial connection. The robot movement is controlled using forward, backward, left, and right commands.
# The robot expects commands through stdin (which can be communicated from a Raspberry Pi via a web interface).

# Importing necessary modules
from XRPLib.defaults import *  # Import robot control library (likely defined elsewhere)
from machine import Timer, UART, Pin  # Microcontroller-specific libraries for hardware control
import select  # For handling non-blocking input from stdin
import sys  # For handling standard input/output
import time  # For controlling delays and time-based logic

# Set up the poll object for detecting incoming data from stdin
poll_obj = select.poll()  # Creates a poll object to manage events
poll_obj.register(sys.stdin, select.POLLIN)  # Register stdin for polling, to check for input availability

# Print startup messages for the user
print('XRP robot at your service!')  # A friendly message indicating the system is ready
print("Awaiting remote commands")  # Ready to receive commands

# Define the function for controlling the motion of the robot
def corr_Motion(command):
    """
    This function takes a single character command (F, B, L, R) and moves the robot accordingly:
    F -> Forward, B -> Backward, L -> Left, R -> Right.
    Any other command will stop the robot.
    """
    if command == 'F':  # Forward command
        drivetrain.set_effort(0.5, 0.5)  # Move forward with equal speed for both motors
        time.sleep(2)  # Allow the robot to move for 2 seconds
        drivetrain.set_effort(0, 0)  # Stop the robot after the movement
        time.sleep(2)  # Wait for 2 seconds before accepting the next command
    
    elif command == 'B':  # Backward command
        drivetrain.set_effort(-0.5, -0.5)  # Move backward with equal speed for both motors
        time.sleep(2)  # Allow the robot to move for 2 seconds
        drivetrain.set_effort(0, 0)  # Stop the robot
        time.sleep(2)  # Wait for 2 seconds before accepting the next command
    
    elif command == 'L':  # Left command
        drivetrain.set_effort(-0.5, 0.5)  # Turn left by rotating wheels in opposite directions
        time.sleep(2)  # Allow the robot to turn for 2 seconds
        drivetrain.set_effort(0, 0)  # Stop the robot
        time.sleep(2)  # Wait for 2 seconds before accepting the next command
    
    elif command == 'R':  # Right command
        drivetrain.set_effort(0.5, -0.5)  # Turn right by rotating wheels in opposite directions
        time.sleep(2)  # Allow the robot to turn for 2 seconds
        drivetrain.set_effort(0, 0)  # Stop the robot
        time.sleep(2)  # Wait for 2 seconds before accepting the next command
    
    else:
        drivetrain.set_effort(0, 0)  # Stop the robot for unknown commands
        time.sleep(5)  # Wait for 5 seconds in case of an invalid command to avoid sudden movements

    return None  # No return value, as the function directly controls the robot's movements

# Main loop to keep the program running and constantly check for incoming data
while True:
    # poll_obj.poll(1000) will wait for data for up to 1000 milliseconds (1 second)
    poll_results = poll_obj.poll(1000)
    
    # If poll_results has data, we read the command from stdin
    if poll_results:
        # Read the data from stdin, strip leading/trailing whitespaces, and process the command
        data = sys.stdin.readline().strip()  # Read and clean up the input
        print(f"\nReceived data: {data}")  # Print the received command for debugging/confirmation
        corr_Motion(data)  # Call the motion function with the received command
    else:
        # No data received; continue the loop and handle other tasks if necessary
        time.sleep(2)  # Sleep for 2 seconds to reduce unnecessary looping and CPU usage
