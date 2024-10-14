# Raspberry Pi side code
# Filename:webjoystickMqttflskTimerSndWkng3.61.py
#Includes timer to neglect mutiple cmds in 1sec
import serial
import time
import paho.mqtt.client as mqtt

# Set up the serial connection to Pico (adjust port and settings if needed)
try:
    s = serial.Serial(port="/dev/ttyACM0", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
    print("Connected to Pico via USB Serial.")
except serial.SerialException as e:
    print(f"Failed to connect to Pico: {e}")
    s = None

# Function to send a message to Pico
def send_msg_pico(data):
    if not s:
        print("Serial connection not established.")
        return
    try:
        s.reset_input_buffer()  # Clear any existing data in the input buffer
        s.write(data.encode('utf-8'))
        print("Sent data to Pico:", data)
    except Exception as e:
        print(f"Error sending data to Pico: {e}")

# MQTT configuration
MQTT_BROKER = "5c4849f0caf34edf9bce57b8bc3f7ff2.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "xrp/commands"
MQTT_USER = "xrphivemq"
MQTT_PASSWORD = "Digikey@2024"

# Initialize the last command time to 0
last_command_time = 0  # Epoch timestamp for the last processed command

# Define the MQTT callback when a message is received
def on_message(client, userdata, msg):
    global last_command_time  # Use the global variable to track time between commands
    try:
        # Decode the received message
        command = msg.payload.decode('utf-8')
        print(f"Received command: {command}")

        # Get the current time in seconds
        current_time = time.time()

        # If more than 1 second has passed since the last command, send the new command
        if current_time - last_command_time > 1:  # 1 second interval
            send_msg_pico(command + '\n')  # Send command to Pico with newline
            last_command_time = current_time  # Update the timestamp
        else:
            print("Command ignored to prevent spamming within 1 second.")

    except Exception as e:
        print(f"Error handling received message: {e}")

# Set up MQTT client
client = mqtt.Client()

# Set up TLS for secure communication with HiveMQ
client.tls_set()  # Consider specifying CA certificates if required by the broker

# Set username and password
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Assign the message callback function
client.on_message = on_message

# Connect to the MQTT broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT)
    print(f"Connected to MQTT Broker: {MQTT_BROKER}")
except Exception as e:
    print(f"Failed to connect to MQTT Broker: {e}")
    exit()

# Subscribe to the command topic
client.subscribe(MQTT_TOPIC)

# Start the MQTT client loop to listen for messages
client.loop_start()

# Main loop to keep the program running
try:
    while True:
        time.sleep(1)  # Keep the main loop alive
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()  # Stop the MQTT client loop
    client.disconnect()  # Disconnect from MQTT broker
    if s:
        s.close()  # Close the serial connection properly
        print("Serial connection closed.")
