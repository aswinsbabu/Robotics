#wsgi.py path: my_proj_env/bin/wsgi.py #google cloud server
from flask import Flask, render_template_string, jsonify
import paho.mqtt.client as mqtt

# Initialize the Flask application
app = Flask(__name__)

# MQTT Broker configuration
MQTT_BROKER = "5c4849f0caf34edf9bce57b8bc3f7ff2.s1.eu.hivemq.cloud"  # HiveMQ Cluster URL
MQTT_PORT = 8883  # TLS MQTT Port
MQTT_USER = "xrphivemq"  # Replace with your HiveMQ username
MQTT_PASSWORD = "Digikey@2024"  # Replace with your HiveMQ password
MQTT_TOPIC = "xrp/commands"  # Topic where commands will be published

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

# Define the home route to render the HTML UI
@app.route("/")
def home():
    # HTML content for the web UI with joystick controls
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Joystick Control</title>
        <style>
            button {
                padding: 20px;
                margin: 10px;
                font-size: 20px;
            }
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }
            .row {
                display: flex;
                justify-content: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to XRP!</h1>
            <div class="row">
                <button onclick="sendCommand('forward')">Forward</button>
            </div>
            <div class="row">
                <button onclick="sendCommand('left')">Left</button>
                <button onclick="sendCommand('stop')">Stop</button>
                <button onclick="sendCommand('right')">Right</button>
            </div>
            <div class="row">
                <button onclick="sendCommand('backward')">Backward</button>
            </div>
        </div>
        <script>
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
        </script>
    </body>
    </html>
    '''
    # Render the HTML content as a string
    return render_template_string(html)

# Define the route to handle joystick commands and publish them to MQTT
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

# Run the Flask app on host 0.0.0.0 and port 80
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)     
