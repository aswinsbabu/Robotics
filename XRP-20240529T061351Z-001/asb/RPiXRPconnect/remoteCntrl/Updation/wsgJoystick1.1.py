# wsgi.py path: my_proj_env/bin/wsgi.py
#joystick instead of buttons
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
    # HTML content with joystick interface
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Joystick Control</title>
        <style>
            body {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            #joystick {
                width: 300px;
                height: 300px;
                position: relative;
            }
        </style>
    </head>
    <body>
        <h1>Joystick Control</h1>
        <div id="joystick"></div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/nipplejs/0.9.0/nipplejs.min.js"></script>
        <script>
            // Initialize the joystick using nipplejs
            var joystick = nipplejs.create({
                zone: document.getElementById('joystick'),
                mode: 'static',
                position: { left: '50%', top: '50%' },
                color: 'green',
                size: 200
            });

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
                    console.log('Command sent: ' + command);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }

            // Handle joystick movements
            joystick.on('move', function (evt, data) {
                var direction = data.direction;

                if (direction) {
                    if (direction.angle === 'up') {
                        sendCommand('forward');
                    } else if (direction.angle === 'down') {
                        sendCommand('backward');
                    } else if (direction.angle === 'left') {
                        sendCommand('left');
                    } else if (direction.angle === 'right') {
                        sendCommand('right');
                    }
                }
            });

            // Handle joystick release (stop command)
            joystick.on('end', function () {
                sendCommand('stop');
            });
        </script>
    </body>
    </html>
    '''
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
