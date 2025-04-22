#XRP Side code
from XRPLib.defaults import *
import time
import select
import sys

# Initialize robot components
#drivetrain = Drivetrain()
print('XRP Robot Ready! Waiting for commands...')

def execute_command(command):
    """Execute movement commands with proper timing"""
    drive_time=1.0
    try:
        if command == 'forward':
            drivetrain.set_effort(0.8, 0.8)
            time.sleep(drive_time)
            drivetrain.stop()
            
        elif command == 'backward':
            drivetrain.set_effort(-0.8, -0.8)
            time.sleep(drive_time)
            drivetrain.stop()
            
        elif command == 'left':
            drivetrain.set_effort(-0.8, 0.8)
            time.sleep(drive_time)
            drivetrain.stop()
            
        elif command == 'right':
            drivetrain.set_effort(0.8, -0.8)
            time.sleep(drive_time)
            drivetrain.stop()
            
        elif command == 'stop':
            drivetrain.set_effort(0, 0)
            time.sleep(drive_time)
            drivetrain.stop()
            
        else:
            print(f"Unknown command: {command}")
    finally:
        drivetrain.set_effort(0, 0)  # Ensure stop after each command

# Set up polling for non-blocking input
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# Main command loop
while True:
    # Check for new commands every 100ms
    poll_results = poll_obj.poll(100)
    
    if poll_results:
        command = sys.stdin.readline().strip().lower()
        print(f"Executing: {command}")
        execute_command(command)
    else:
        # Optional idle behavior
        time.sleep(0.1)
