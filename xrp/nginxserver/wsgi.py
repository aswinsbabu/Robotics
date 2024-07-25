from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
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
    return render_template_string(html)

@app.route("/<command>", methods=['POST'])
def handle_command(command):
    try:
        if command in ["forward", "backward", "left", "right", "stop"]:
            # Placeholder for sending command to the XRP robot
            print(f"Command received: {command}")
            return jsonify(success=True, message=f"Command {command} sent")
        else:
            return jsonify(success=False, message="Invalid command")
    except Exception as e:
        return jsonify(success=False, message=str(e))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)