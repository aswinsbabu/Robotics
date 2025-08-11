from XRP import *
import time

xrp = XRP()  # Initialize robot

while True:
    xrp.set_motors(0.5, 0.5)  # Forward
    time.sleep(2)
    xrp.set_motors(-0.5, -0.5)  # Backward
    time.sleep(2)
    xrp.set_motors(0, 0)        # Stop
    time.sleep(1)