import select
import sys
import time

# Set up the poll object for detecting incoming data
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)  # Register stdin for polling

# Loop indefinitely to check for incoming data
while True:
    poll_results = poll_obj.poll(1000)  # Wait for data for 1000 milliseconds (1 second)
    if poll_results:
        # Read the data from stdin and strip whitespace/newline
        data = sys.stdin.readline().strip()
        # Print or process received data; adjust stdout use if issues arise
        print(f"\nReceived data: {data}")
    else:
        # No data received; continue loop or handle other tasks
        print("No data received, waiting...")
        time.sleep(1)  # Delay to reduce unnecessary looping

