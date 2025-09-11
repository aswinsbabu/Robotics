import time
import board
import digitalio
from XRPLib.defaults import *

class UltrasonicSensor:
    """
    Class to interface with RCWL-1601 ultrasonic sensor
    """
    def __init__(self, trigger_pin, echo_pin, timeout=1.0):
        """
        Initialize ultrasonic sensor
        
        Args:
            trigger_pin: Board pin for trigger (e.g., board.IO0)
            echo_pin: Board pin for echo (e.g., board.IO1) 
            timeout: Maximum time to wait for echo (seconds)
        """
        self.trigger = digitalio.DigitalInOut(trigger_pin)
        self.trigger.direction = digitalio.Direction.OUTPUT
        
        self.echo = digitalio.DigitalInOut(echo_pin)
        self.echo.direction = digitalio.Direction.INPUT
        
        self.timeout = timeout
        
    def get_distance(self):
        """
        Get distance measurement in centimeters
        
        Returns:
            Distance in cm, or None if measurement fails
        """
        # Send 10us trigger pulse
        self.trigger.value = False
        time.sleep(0.000002)  # 2us
        self.trigger.value = True
        time.sleep(0.00001)   # 10us
        self.trigger.value = False
        
        # Wait for echo to go high
        start_time = time.monotonic()
        while not self.echo.value:
            if time.monotonic() - start_time > self.timeout:
                return None  # Timeout
        
        # Measure echo pulse duration
        pulse_start = time.monotonic()
        while self.echo.value:
            if time.monotonic() - pulse_start > self.timeout:
                return None  # Timeout
        pulse_end = time.monotonic()
        
        # Calculate distance
        # Speed of sound = 343 m/s = 0.0343 cm/us
        # Distance = (pulse_duration * speed_of_sound) / 2
        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 34300) / 2  # in cm
        
        return round(distance, 2)

class ObstacleAvoidanceRobot:
    """
    XRP Robot with obstacle avoidance using ultrasonic sensor
    """
    def __init__(self):
        # Initialize XRP components
        self.drivetrain = Drivetrain()
        self.board_led = boardLED()
        
        # Initialize ultrasonic sensor (adjust pins as needed)
        self.sensor = UltrasonicSensor(board.IO0, board.IO1)
        
        # Configuration
        self.safe_distance = 20.0  # cm
        self.move_speed = 30       # motor speed percentage
        self.turn_time = 0.8       # seconds to turn
        
    def scan_distance(self):
        """Get distance reading with error handling"""
        distance = self.sensor.get_distance()
        if distance is None:
            print("Sensor reading failed")
            return float('inf')  # Treat as no obstacle
        return distance
    
    def obstacle_detected(self):
        """Check if obstacle is within safe distance"""
        distance = self.scan_distance()
        print(f"Distance: {distance} cm")
        return distance < self.safe_distance
    
    def move_forward(self):
        """Move robot forward"""
        self.drivetrain.set_speed(self.move_speed, self.move_speed)
        self.board_led.on()
    
    def stop(self):
        """Stop robot movement"""
        self.drivetrain.stop()
        self.board_led.off()
    
    def turn_right(self):
        """Turn robot right"""
        print("Turning right...")
        self.drivetrain.set_speed(self.move_speed, -self.move_speed)
        time.sleep(self.turn_time)
        self.stop()
    
    def turn_left(self):
        """Turn robot left"""
        print("Turning left...")
        self.drivetrain.set_speed(-self.move_speed, self.move_speed)
        time.sleep(self.turn_time)
        self.stop()
    
    def backup(self):
        """Move robot backward briefly"""
        print("Backing up...")
        self.drivetrain.set_speed(-self.move_speed, -self.move_speed)
        time.sleep(0.5)
        self.stop()
    
    def run_obstacle_avoidance(self):
        """Main obstacle avoidance loop"""
        print("Starting obstacle avoidance...")
        
        try:
            while True:
                if self.obstacle_detected():
                    print("Obstacle detected!")
                    self.stop()
                    self.backup()
                    
                    # Randomly choose turn direction
                    import random
                    if random.choice([True, False]):
                        self.turn_right()
                    else:
                        self.turn_left()
                    
                    # Brief pause before continuing
                    time.sleep(0.2)
                else:
                    print("Path clear, moving forward")
                    self.move_forward()
                
                time.sleep(0.1)  # Small delay between readings
                
        except KeyboardInterrupt:
            print("Stopping robot...")
            self.stop()

# Simple distance monitoring function
def distance_monitor():
    """Simple function to continuously monitor distance"""
    sensor = UltrasonicSensor(board.IO0, board.IO1)
    led = boardLED()
    
    print("Distance Monitor Started (Ctrl+C to stop)")
    
    try:
        while True:
            distance = sensor.get_distance()
            if distance is not None:
                print(f"Distance: {distance:.2f} cm")
                
                # Light LED if object is close
                if distance < 15:
                    led.on()
                else:
                    led.off()
            else:
                print("Measurement failed")
                
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("Monitoring stopped")
        led.off()

# Example usage
if __name__ == "__main__":
    # Option 1: Run obstacle avoidance robot
    robot = ObstacleAvoidanceRobot()
    robot.run_obstacle_avoidance()
    
    # Option 2: Just monitor distance (uncomment to use)
    # distance_monitor()
    
    
