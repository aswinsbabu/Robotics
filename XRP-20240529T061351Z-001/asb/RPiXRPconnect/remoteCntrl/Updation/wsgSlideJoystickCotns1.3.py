#File: wsgSlideJoystickCotns1.3.py
#Sends continous commands as long as joystick pressed
# wsgi.py path: my_proj_env/bin/wsgi.py==>Git Robotics/XRP-20240529T061351Z-001/asb/RPiXRPconnect/remoteCntrl/Updation/wsgSlideJoystickCotns1.3.py
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
        
        <!-- Include nipplejs library to create joystick -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/nipplejs/0.9.0/nipplejs.min.js"></script>
        
        <script>
            // Create joystick using nipplejs
            var joystick = nipplejs.create({
                zone: document.getElementById('joystick'), // Attach to the 'joystick' div
                mode: 'static', // Joystick will remain in one fixed position
                position: { left: '50%', top: '50%' }, // Center the joystick in the div
                color: 'green', // Color of the joystick handle
                size: 200 // Diameter of the joystick
            });

            // Function to send a command to the server via fetch API
            function sendCommand(command) {
                // POST the command to the Flask server's /<command> route
                fetch('/' + command, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                })
                .then(response => response.json())
                .then(data => {
                    // Log the command for debugging purposes
                    console.log('Command sent: ' + command);
                })
                .catch(error => {
                    // Log any errors
                    console.error('Error:', error);
                });
            }

            // Function to handle continuous joystick movements
            joystick.on('move', function (evt, data) {
                // 'data.direction' contains the direction of movement
                var direction = data.direction;

                // Check if the direction exists (to avoid errors)
                if (direction) {
                    // Based on the angle of the joystick, send corresponding commands
                    if (direction.angle === 'up') {
                        sendCommand('forward');  // Joystick pushed up -> Send 'forward' command
                    } else if (direction.angle === 'down') {
                        sendCommand('backward'); // Joystick pushed down -> Send 'backward' command
                    } else if (direction.angle === 'left') {
                        sendCommand('left');     // Joystick pushed left -> Send 'left' command
                    } else if (direction.angle === 'right') {
                        sendCommand('right');    // Joystick pushed right -> Send 'right' command
                    }
                }
            });

            // Function to handle joystick release
            joystick.on('end', function () {
                // When the joystick is released, send the 'stop' command
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
        "forward": "F",  # Forward command mapped to 'F'
        "backward": "B", # Backward command mapped to 'B'
        "left": "L",     # Left command mapped to 'L'
        "right": "R",    # Right command mapped to 'R'
        "stop": "S"      # Stop command mapped to 'S'
    }

    try:
        # Check if the command is valid and mapped to an MQTT message
        if command in command_map:
            mqtt_message = command_map[command]  # Get the MQTT message for the command
            # Publish the mapped command to the specified MQTT topic
            client.publish(MQTT_TOPIC, mqtt_message)
            print(f"Command received: {command}, sent as MQTT message: {mqtt_message}")
            return jsonify(success=True, message=f"Command {command} sent as {mqtt_message}")
        else:
            return jsonify(success=False, message="Invalid command")  # Handle invalid commands
    except Exception as e:
        # Return the exception message in case of an error
        return jsonify(success=False, message=str(e))

# Run the Flask app on host 0.0.0.0 and port 80
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)


'''
Frontend (HTML and JavaScript):
NippleJS Setup:

joystick.on('move'): Handles joystick movements. Whenever the joystick is moved, the direction (up, down, left, right) is detected.
joystick.on('end'): Handles when the joystick is released. When the user releases the joystick, it automatically sends the stop command.
Continuous Commands:

As long as the joystick is being moved in a direction, it will continuously send the corresponding command to the server.
When the joystick is released, a stop command is sent to signal stopping the movement.


Backend (Python and Flask):
MQTT Message Handling:
The Flask route /command handles incoming joystick commands (forward, backward, left, right, stop).
These commands are mapped to corresponding MQTT messages (F, B, L, R, S) and published to the specified MQTT topic.
This implementation ensures that the system reacts in real-time as long as the joystick is pressed and stops when it is released.
'''
