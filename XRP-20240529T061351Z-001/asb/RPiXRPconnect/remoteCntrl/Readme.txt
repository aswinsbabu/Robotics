Reference URL
https://docs.google.com/document/d/1_A1Lv02Be2mTH6Z1uLA7kcMG9da5OztheT991mca-7k/edit#heading=h.ilw1uc7rijph 

Webserver code explanation
Here's an explanation of each section of the provided code:

### Import Libraries
```python
from flask import Flask, render_template_string, jsonify
import paho.mqtt.client as mqtt
```
- Imports Flask modules for creating a web server (`Flask`), rendering HTML directly from strings (`render_template_string`), and returning JSON responses (`jsonify`).
- Imports the `paho.mqtt.client` library for MQTT (Message Queuing Telemetry Transport) to handle messaging.

### Flask Application Initialization
```python
# Initialize the Flask application
app = Flask(__name__)
```
- Creates an instance of the Flask application.

### MQTT Configuration
```python
# MQTT Broker configuration
MQTT_BROKER = "5c4849f0caf34edf9bce57b8bc3f7ff2.s1.eu.hivemq.cloud"  # HiveMQ Cluster URL
MQTT_PORT = 8883  # TLS MQTT Port
MQTT_USER = "xrphivemq"  # Replace with your HiveMQ username
MQTT_PASSWORD = "Digikey@2024"  # Replace with your HiveMQ password
MQTT_TOPIC = "xrp/commands"  # Topic where commands will be published
```
- Sets up the MQTT broker's URL, port, user credentials, and the topic to which messages will be published.

### MQTT Client Initialization
```python
# Initialize the MQTT client
client = mqtt.Client()

# Enable TLS for secure communication
client.tls_set()  # Uses default CA certs; adjust if specific certs are needed

# Set the username and password for the MQTT connection
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Connect to the MQTT Broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT)
    print(f"Connected to MQTT Broker: {MQTT_BROKER}")
except Exception as e:
    print(f"Failed to connect to MQTT Broker: {e}")
```
- Initializes an MQTT client, sets up TLS for secure communication, and connects to the broker using the given credentials. It handles exceptions if the connection fails.

### Flask Home Route (Web Interface)
```python
@app.route("/")
def home():
    # HTML content for the web UI with joystick controls
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    ...
    </html>
    '''
    # Render the HTML content as a string
    return render_template_string(html)
```
- Defines the root route (`/`) that serves a web interface for controlling the system. The interface has buttons for joystick controls (`Forward`, `Backward`, `Left`, `Right`, `Stop`), which send commands to the server when clicked.

### JavaScript Code (Embedded in HTML)
```javascript
// Function to send a command to the server
function sendCommand(command) {
    fetch('/' + command, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
           alert('Command sent: ' + command);
        } else {
            alert('Error sending command: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred.');
    });
}
```
- Defines a JavaScript function that sends a POST request to the server with the selected command (`Forward`, `Backward`, etc.). It handles the response and displays an alert indicating success or failure.

### Flask Command Handling Route
```python
@app.route("/<command>", methods=['POST'])
def handle_command(command):
    # Map the received command to MQTT messages
    command_map = {
        "forward": "F",
        "backward": "B",
        "left": "L",
        "right": "R",
        "stop": "S"
    }

    try:
        # Check if the command is valid and mapped to an MQTT message
        if command in command_map:
            mqtt_message = command_map[command]
            # Publish the mapped command to the specified MQTT topic
            client.publish(MQTT_TOPIC, mqtt_message)
            print(f"Command received: {command}, sent as MQTT message: {mqtt_message}")
            return jsonify(success=True, message=f"Command {command} sent as {mqtt_message}")
        else:
            return jsonify(success=False, message="Invalid command")
    except Exception as e:
        # Return the exception message in case of an error
        return jsonify(success=False, message=str(e))
```
- This route handles incoming commands from the JavaScript function and maps them to corresponding MQTT messages. If the command is valid, it publishes the message to the MQTT topic; otherwise, it returns an error.

### Flask Application Execution
```python
# Run the Flask app on host 0.0.0.0 and port 80
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
```
- Runs the Flask application on all available IP addresses (`0.0.0.0`) and listens on port 80, making it accessible over the network.

### Summary
- **Purpose**: The code sets up a web interface using Flask to control a system via joystick-like commands. The commands are sent to a Raspberry Pi or another device using MQTT.
- **Web Interface**: Provides a simple UI with buttons to control movement.
- **MQTT Integration**: Sends control commands via MQTT for remote control of devices, ensuring secure communication through TLS.
