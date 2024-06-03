from XRPLib.defaults import *
import time

while True:
    left_encoder = drivetrain.get_left_encoder_position()
    right_encoder = drivetrain.get_right_encoder_position()
    imu_heading = imu.get_heading()
    print(f"Encoder Left: {left_encoder}\tEncoder Right: {right_encoder}\tIMU Heading: {imu_heading}")
    time.sleep(0.5)
