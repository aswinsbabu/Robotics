#Raspberry Pi Side code: 1.41_RpiKidsProgramUI_CodeGenNwkng.py
#Close button on tiles
#Clear CodeGen Zone
# Fixed generated code syntax on UI(No if loop)

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

        .command-tile span {
            display: inline-block;
            transition: all 0.2s ease;
        }

        .command-tile span:hover {
            color: #ff0000 !important;
            font-size: 32px !important;
            transform: scale(1.2);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Student's Programming</h1>
        <img src="https://cdn-icons-png.flaticon.com/512/2593/2593308.png" class="robot-img" alt="Robot">
        <h2>Drag-and-Drop Commands</h2>
    </div>

    <div class="palette">
        <div class="command-tile" draggable="true" data-command="forward">FORWARD</div>
        <div class="command-tile" draggable="true" data-command="backward">BACKWARD</div>
        <div class="command-tile" draggable="true" data-command="left">LEFT</div>
        <div class="command-tile" draggable="true" data-command="right">RIGHT</div>
        <div class="command-tile" draggable="true" data-command="stop">STOP</div>
    </div>

    <div class="zones-container">
        <div class="drop-zone" id="dropZone">
            🎯 Drop commands here to build your program!
        </div>

        <div class="code-generator" id="codeZone">
            🎯 See the code corresponding to your block program!
        </div>
    </div>

    <button id="program-btn" onclick="sendProgram()">PROGRAM ROBOT!</button>
    <button id="clear-btn" onclick="clearProgram()">CLEAR</button>

    <script>
        const codeSnippets = {
            forward: `
        #corresponding code for 'forward'
            drivetrain.set_effort(0.8, 0.8)   #Set effort for left and right motors
            time.sleep(1)
            drivetrain.stop()
        `,

            backward: `
        #corresponding code for 'backward'
            drivetrain.set_effort(-0.8, -0.8) #Set effort to negative for going backward
            time.sleep(1)
            drivetrain.stop()
        `,

            left: `
        #corresponding code for 'left'
            drivetrain.set_effort(-0.8, 0.8)  #Left wheel backward and right forward for left turn
            time.sleep(1)
            drivetrain.stop()
        `,

            right: `
        #corresponding code for 'right'
            drivetrain.set_effort(0.8, -0.8)  #Right wheel backward and left forward for right turn
            time.sleep(1)
            drivetrain.stop()
        `,

            stop: `
        #corresponding code for 'stop'
            drivetrain.set_effort(0, 0)       #Set effort on both wheel to zero to stop
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

            // Create close button (X)
            const closeBtn = document.createElement('span');
            closeBtn.textContent = ' x';
            closeBtn.style.cursor = 'pointer';
            closeBtn.style.marginLeft = '10px';
            closeBtn.style.color = '#ff6b6b';
            closeBtn.style.fontWeight = 'bold';
            closeBtn.style.fontSize = '28px';
            closeBtn.title = 'Remove this command';

            // Store the current index before adding to array
            commandList.push(command);
            const commandIndex = commandList.length - 1;

            // Add the close button to the command tile
            tile.appendChild(closeBtn);

            // Add the tile to the drop zone
            dropZone.appendChild(tile);

            // Display corresponding Python code in the code generator zone
            const codeZone = document.getElementById('codeZone');
            const codeLine = document.createElement('pre');
            codeLine.textContent = codeSnippets[command] || '# Unknown command';
            codeLine.className = 'code-line';
            codeLine.dataset.index = commandIndex; // Tag with index for easy removal
            codeZone.appendChild(codeLine);

            // Add event handler for close button
            closeBtn.onclick = function(event) {
                event.stopPropagation(); // Prevent event bubbling
                
                // Remove the tile from DOM
                tile.remove();
                
                // Remove from commandList
                commandList[commandIndex] = null;
                
                // Remove corresponding code block
                const codeBlock = codeZone.querySelector(`[data-index="${commandIndex}"]`);
                if (codeBlock) {
                    codeBlock.remove();
                }
            };
        }

        function sendProgram() {
            const filteredCommands = commandList.filter(cmd => cmd !== null);
            if (filteredCommands.length === 0) {
                alert('Please add some commands first!');
                return;
            }
            fetch('/execute', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(filteredCommands)
            })
            .then(response => alert('Program sent to robot!'))
            .catch(err => alert('Error sending program'));
        }

        function clearProgram() {
            dropZone.innerHTML = '🎯 Drop commands here to build your program!';
            document.getElementById('codeZone').innerHTML = '🎯 See the code corresponding to your block program!';
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
    
