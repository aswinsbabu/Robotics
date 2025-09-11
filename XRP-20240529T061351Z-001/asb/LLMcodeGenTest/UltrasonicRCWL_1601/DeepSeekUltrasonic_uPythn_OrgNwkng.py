#Using Micro Python Libraries
from machine import Pin, time_pulse_us
import time

class RCWL1601Ultrasonic:
    def __init__(self, trig_pin, echo_pin):
        """
        Initialize the ultrasonic sensor
        
        Args:
            trig_pin: GPIO pin number for TRIG
            echo_pin: GPIO pin number for ECHO
        """
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.trig.value(0)
        self.timeout = 30000  # Timeout in microseconds (30ms)
        
    def distance_cm(self):
        """
        Measure distance in centimeters
        
        Returns:
            Distance in cm or None if measurement fails
        """
        # Send trigger pulse
        self.trig.value(1)
        time.sleep_us(10)  # 10 microsecond pulse
        self.trig.value(0)
        
        try:
            # Measure the pulse duration on ECHO pin
            pulse_time = time_pulse_us(self.echo, 1, self.timeout)
            
            # Calculate distance (speed of sound = 343 m/s = 0.0343 cm/us)
            # Distance = (time * speed) / 2 (round trip)
            distance = (pulse_time * 0.0343) / 2
            
            return round(distance, 2)
            
        except OSError:  # Timeout occurred
            return None

# Main program for XRP robot integration
class XRPUltrasonicRobot:
    def __init__(self):
        # Initialize ultrasonic sensor (adjust pins as needed)
        self.ultrasonic = RCWL1601Ultrasonic(trig_pin=15, echo_pin=14)
        
        # You can add XRP motor control initialization here
        # from xrp import Motor, Servo, etc.
        
        # Distance thresholds (in cm)
        self.obstacle_distance = 20
        self.safe_distance = 30
        
    def measure_distance(self, samples=3):
        """
        Take multiple measurements and return average
        
        Args:
            samples: Number of measurements to average
            
        Returns:
            Average distance in cm
        """
        distances = []
        for _ in range(samples):
            dist = self.ultrasonic.distance_cm()
            if dist is not None and 2 < dist < 400:  # Valid range
                distances.append(dist)
            time.sleep(0.05)  # Short delay between measurements
        
        if distances:
            return sum(distances) / len(distances)
        return None
    
    def obstacle_detection(self):
        """
        Simple obstacle detection routine
        Returns True if obstacle is detected within threshold distance
        """
        distance = self.measure_distance()
        if distance is not None and distance < self.obstacle_distance:
            return True, distance
        return False, distance
    
    def run_avoidance_demo(self):
        """
        Demo function for obstacle avoidance
        (You'll need to implement actual motor control)
        """
        print("Starting obstacle avoidance demo...")
        
        try:
            while True:
                obstacle, distance = self.obstacle_detection()
                
                if obstacle:
                    print(f"Obstacle detected at {distance} cm! Taking evasive action.")
                    # Add your avoidance logic here
                    # Example: stop, reverse, turn
                    # self.motors.stop()
                    # time.sleep(1)
                    # self.motors.turn_right(0.5)
                    
                else:
                    print(f"Clear path: {distance} cm ahead")
                    # Continue moving forward
                    # self.motors.forward(0.3)
                
                time.sleep(0.5)  # Check every 0.5 seconds
                
        except KeyboardInterrupt:
            print("Demo stopped")
            # self.motors.stop()

# Example usage and testing
def test_ultrasonic():
    """Simple test function for the ultrasonic sensor"""
    sensor = RCWL1601Ultrasonic(trig_pin=20, echo_pin=21)
    
    print("Testing RCWL-1601 Ultrasonic Sensor")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            distance = sensor.distance_cm()
            if distance is not None:
              
                print(f"Distance: {distance} cm")
            else:
                print("Measurement failed or out of range")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Test stopped")

# Main execution
if __name__ == "__main__":
    # Uncomment for simple sensor test
    # test_ultrasonic()
    
    # Create robot instance and run demo
    robot = XRPUltrasonicRobot()
    
    # Quick distance measurement test
    print("Testing distance measurement...")
    for i in range(5):
        dist = robot.measure_distance()
        print(f"Measurement {i+1}: {dist} cm")
        time.sleep(1)
    
    # Uncomment to run the avoidance demo (requires motor control implementation)
    # robot.run_avoidance_demo()