import wpilib
import time

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize digital pins for RCWL-1601
        self.trigPin = wpilib.DigitalOutput(3)  # Trigger pin (GPIO 3)
        self.echoPin = wpilib.DigitalInput(2)   # Echo pin (GPIO 2)
        
        # Initialize drivetrain (assuming XRP differential drive)
        self.leftMotor = wpilib.PWMVictorSPX(0)  # Left motor PWM channel
        self.rightMotor = wpilib.PWMVictorSPX(1) # Right motor PWM channel
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotor, self.rightMotor)
        
        # Constants for distance calculation
        self.SPEED_OF_SOUND = 343  # Speed of sound in m/s
        self.DISTANCE_THRESHOLD = 0.5  # Stop if obstacle closer than 0.5m

    def getDistance(self):
        # Send 10us trigger pulse
        self.trigPin.set(False)
        time.sleep(0.000002)  # 2us low
        self.trigPin.set(True)
        time.sleep(0.00001)   # 10us high
        self.trigPin.set(False)
        
        # Measure echo pulse duration
        startTime = time.time()
        timeout = startTime + 0.1  # 100ms timeout
        
        # Wait for echo to go high
        while not self.echoPin.get() and time.time() < timeout:
            pass
        startTime = time.time()
        
        # Wait for echo to go low
        while self.echoPin.get() and time.time() < timeout:
            pass
        endTime = time.time()
        
        # Calculate distance (distance = speed * time / 2)
        pulseDuration = endTime - startTime
        distance = (pulseDuration * self.SPEED_OF_SOUND) / 2  # Convert to meters
        
        return distance if distance > 0 and distance < 4.5 else -1  # Return -1 if out of range (2cm-450cm)

    def teleopPeriodic(self):
        # Get distance from sensor
        distance = self.getDistance()
        
        # Print distance for debugging
        if distance >= 0:
            wpilib.SmartDashboard.putNumber("Distance (m)", distance)
        else:
            wpilib.SmartDashboard.putString("Distance", "Out of range")
        
        # Simple obstacle avoidance: stop if too close, else move forward
        if distance >= 0 and distance < self.DISTANCE_THRESHOLD:
            self.drive.tankDrive(0, 0)  # Stop
        else:
            self.drive.tankDrive(0.5, 0.5)  # Move forward at half speed

if __name__ == "__main__":
    wpilib.run(MyRobot)
    