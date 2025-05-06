#1.2 XRP Side code
#Modified to send executed commands back to RPi

from XRPLib.defaults import *
import time
import select
import sys

# Initialize robot components
#drivetrain = Drivetrain()
print('XRP Robot Ready! Waiting for commands...')

# Modified execute_command function
executed_lines = []

def execute_command(command):
    """Execute movement commands with proper timing"""
    global executed_lines
    drive_time = 1.0
    try:
        if command == 'forward':
            executed_lines.append("drivetrain.set_effort(0.8, 0.8)")
            drivetrain.set_effort(0.8, 0.8)
            time.sleep(drive_time)
            executed_lines.append("drivetrain.stop()")
            drivetrain.stop()
            
        elif command == 'backward':
            executed_lines.append("drivetrain.set_effort(-0.8, -0.8)")
            drivetrain.set_effort(-0.8, -0.8)
            time.sleep(drive_time)
            executed_lines.append("drivetrain.stop()")
            drivetrain.stop()
            
        elif command == 'left':
            executed_lines.append("drivetrain.set_effort(-0.8, 0.8)")
            drivetrain.set_effort(-0.8, 0.8)
            time.sleep(drive_time)
            executed_lines.append("drivetrain.stop()")
            drivetrain.stop()
            
        elif command == 'right':
            executed_lines.append("drivetrain.set_effort(0.8, -0.8)")
            drivetrain.set_effort(0.8, -0.8)
            time.sleep(drive_time)
            executed_lines.append("drivetrain.stop()")
            drivetrain.stop()
            
        elif command == 'stop':
            executed_lines.append("drivetrain.set_effort(0, 0)")
            drivetrain.set_effort(0, 0)
            time.sleep(drive_time)
            executed_lines.append("drivetrain.stop()")
            drivetrain.stop()
            
        else:
            executed_lines.append(f"print('Unknown command: {command}')")
            print(f"Unknown command: {command}")
    finally:
        executed_lines.append("drivetrain.set_effort(0, 0)")
        drivetrain.set_effort(0, 0)  # Ensure stop after each command

# Add functionality to send executed lines via serial
def send_executed_lines(serial_conn):
    """Send executed lines of code to Raspberry Pi"""
    global executed_lines
    if executed_lines:
        serial_conn.write("\n".join(executed_lines).encode())
        executed_lines = []  # Clear the log after sending
        

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
