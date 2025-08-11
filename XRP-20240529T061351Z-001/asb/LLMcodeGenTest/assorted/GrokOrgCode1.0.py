import wpilib
import wpilib.drive
import time

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize motors (assuming standard XRP motor ports)
        self.leftMotor = wpilib.PWMSparkMax(0)  # Left motor on PWM port 0
        self.rightMotor = wpilib.PWMSparkMax(1)  # Right motor on PWM port 1
        # Create DifferentialDrive object for tank-style driving
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotor, self.rightMotor)

    def autonomousInit(self):
        # Called when autonomous mode starts
        self.timer = wpilib.Timer()
        self.timer.start()

    def autonomousPeriodic(self):
        # Move forward for 3 seconds at 50% speed
        if self.timer.get() < 3.0:
            self.drive.tankDrive(0.5, 0.5)  # Both motors forward
        # Stop for 1 second
        elif self.timer.get() < 4.0:
            self.drive.tankDrive(0.0, 0.0)  # Stop motors
        # Move backward for 3 seconds at 50% speed
        elif self.timer.get() < 7.0:
            self.drive.tankDrive(-0.5, -0.5)  # Both motors backward
        else:
            self.drive.tankDrive(0.0, 0.0)  # Stop motors

if __name__ == "__main__":
    wpilib.run(MyRobot)