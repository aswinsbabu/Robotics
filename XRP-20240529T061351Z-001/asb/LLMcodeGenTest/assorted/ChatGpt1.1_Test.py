'''Change 1'''
#from xrplib.defaults import drivetrain
from XRPLib.defaults import drivetrain
import time

# Move forward
drivetrain.set_effort(0.8, 0.8)
time.sleep(1)
drivetrain.stop()

# Wait before moving backward
time.sleep(0.5)

# Move backward
drivetrain.set_effort(-0.8, -0.8)
time.sleep(1)
drivetrain.stop()
