#Raspberry Pi Side code: Adjacent Zones

from flask import Flask, request, jsonify
import serial
import time
import threading
import serial.tools.list_ports

app = Flask(__name__)

# Serial port configuration
SERIAL_PORT = '/dev/ttyACM0'  # Default serial port for XRP robot
BAUD_RATE = 115200           # Standard baud rate for serial communication

def find_xrp_port():
    """Auto-detect XRP robot's serial port by checking connected devices"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "ACM" in port.device or "USB" in port.description:  # Common XRP identifiers
            return port.device
    return None  # Return None if not found



# Embedded HTML/JS/CSS for the web interface
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student's Programming - XRP Robot</title>
    <style>
        body {
            font-family: 'Comic Sans MS', cursive;
            background: #f0f9ff;
            margin: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .robot-img {
            width: 150px;
            margin: 20px;
        }
        .palette {
            background: #fff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .command-tile {
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 15px 25px;
            margin: 10px;
            border-radius: 10px;
            cursor: move;
            font-size: 24px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        .command-tile:hover {
            transform: scale(1.1);
        }

        .zones-container {
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }

        .drop-zone,
        .code-generator {
            flex: 1;
            min-height: 150px;
            background: #e3f2fd;
            border: 3px dashed #2196F3;
            border-radius: 15px;
            padding: 20px;
        }

        #program-btn, #clear-btn {
            background: #FF4081;
            color: white;
            padding: 15px 30px;
            font-size: 24px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin: 10px;
        }
        .sequence-tile {
            background: #2196F3 !important;
            margin: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧑💻 Student's Programming</h1>
        <img src="https://cdn-icons-png.flaticon.com/512/2593/2593308.png" class="robot-img" alt="Robot">
        <h2>Drag-and-Drop Commands</h2>
    </div>

    <div class="palette">
        <div class="command-tile" draggable="true" data-command="forward">⬆️ FORWARD</div>
        <div class="command-tile" draggable="true" data-command="backward">⬇️ BACKWARD</div>
        <div class="command-tile" draggable="true" data-command="left">⬅️ LEFT</div>
        <div class="command-tile" draggable="true" data-command="right">➡️ RIGHT</div>
        <div class="command-tile" draggable="true" data-command="stop">⏹ STOP</div>
    </div>

    <div class="zones-container">
        <div class="drop-zone" id="dropZone">
            🎯 Drop commands here to build your program!
        </div>

        <div class="code-generator" id="codeZone">
            🎯 See the code corresponding to your block program!
        </div>
    </div>

    <button id="program-btn" onclick="sendProgram()">🤖 PROGRAM ROBOT!</button>
    <button id="clear-btn" onclick="clearProgram()">🧹 CLEAR</button>

    <script>
        // Code to be copied
        const codeSnippets = {
            forward: `
        if command == 'forward':
            drivetrain.set_effort(0.8, 0.8)
            time.sleep(1)
            drivetrain.stop()
        `,

            backward: `
        elif command == 'backward':
            drivetrain.set_effort(-0.8, -0.8)
            time.sleep(1)
            drivetrain.stop()
        `,

            left: `
        elif command == 'left':
            drivetrain.set_effort(-0.8, 0.8)
            time.sleep(1)
            drivetrain.stop()
        `,

            right: `
        elif command == 'right':
            drivetrain.set_effort(0.8, -0.8)
            time.sleep(1)
            drivetrain.stop()
        `,

            stop: `
        elif command == 'stop':
            drivetrain.set_effort(0, 0)
            time.sleep(1)
            drivetrain.stop()
        `
        };
        let commandList = [];

        document.querySelectorAll('.command-tile').forEach(tile => {
            tile.addEventListener('dragstart', e => {
                e.dataTransfer.setData('text/plain', e.target.dataset.command);
            });
        });

        const dropZone = document.getElementById('dropZone');

        dropZone.addEventListener('dragover', e => {
            e.preventDefault();
            e.target.style.backgroundColor = '#bbdefb';
        });

        dropZone.addEventListener('drop', e => {
            e.preventDefault();
            const command = e.dataTransfer.getData('text/plain');
            addCommandToSequence(command);
            e.target.style.backgroundColor = '#e3f2fd';
        });

        function addCommandToSequence(command) {
            const tile = document.createElement('div');
            tile.className = 'command-tile sequence-tile';
            tile.textContent = command.toUpperCase();
            tile.dataset.command = command;
            dropZone.appendChild(tile);
            commandList.push(command);
            
            
            // Display corresponding Python code in the code generator zone
            const codeZone = document.getElementById('codeZone');
            const codeLine = document.createElement('pre'); //preparing a container to hold the Python code snippet
            codeLine.textContent = codeSnippets[command] || '# Unknown command'; //sets the text inside the <pre> element.
            codeZone.appendChild(codeLine); //adds the new <pre> element (with the Python code inside it) to the codeZone area

        }

        function sendProgram() {
            fetch('/execute', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(commandList)
            })
            .then(response => alert('Program sent to robot! 🤖'))
            .catch(err => alert('Error sending program 😢'));
        }

        function clearProgram() {
            dropZone.innerHTML = '🎯 Drop commands here to build your program!';
            commandList = [];
        }
        
        
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Serve the main interface"""
    return HTML

@app.route('/execute', methods=['POST'])
def execute_program():
    """Handle program execution by sending commands to robot"""
    try:
        commands = request.get_json()  # Get command sequence
        port = find_xrp_port() or SERIAL_PORT  # Auto-detect or use default
        
        with serial.Serial(port, BAUD_RATE, timeout=1) as ser:
            for cmd in commands:
                ser.write(f"{cmd}\n".encode())  # Send each command
                time.sleep(0.8)  # Short delay between commands
                
                
        return jsonify(success=True)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    # Start Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)
    

