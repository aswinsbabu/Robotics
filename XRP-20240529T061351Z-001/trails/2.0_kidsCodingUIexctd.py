#executed code 
#hotspot setup
from XRPLib.defaults import *
import time
import json
import _thread
from machine import Timer

# Optimized HTML for low-memory devices
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Robot Programming</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #f0f0f0; }
        .container { display: flex; flex-direction: row; justify-content: center; align-items: center; }
        .palette, .sequence { display: flex; flex-direction: column; padding: 10px; border: 2px solid black; min-height: 300px; }
        .arrow { padding: 10px; margin: 5px; border: 1px solid black; cursor: grab; background: white; }
        #play { padding: 10px; background: green; color: white; font-size: 18px; cursor: pointer; margin-top: 10px; }
    </style>
</head>
<body>
    <h2>Robot Drag-and-Drop Programming</h2>
    <div class="container">
        <div class="palette">
            <div class="arrow" data-command="forward" draggable="true">^</div>
            <div class="arrow" data-command="backward" draggable="true">v</div>
            <div class="arrow" data-command="left" draggable="true"><</div>
            <div class="arrow" data-command="right" draggable="true">></div>
        </div>
        <div class="sequence" id="sequence-area">Drop commands here</div>
    </div>
    <button id="play">Start</button>

    <script>
        const sequenceArea = document.getElementById("sequence-area");
        let commandList = [];

        document.querySelectorAll(".arrow").forEach(arrow => {
            arrow.addEventListener("dragstart", function(e) {
                e.dataTransfer.setData("command", this.getAttribute("data-command"));
            });
        });

        sequenceArea.addEventListener("dragover", function(e) {
            e.preventDefault();
        });

        sequenceArea.addEventListener("drop", function(e) {
            e.preventDefault();
            const command = e.dataTransfer.getData("command");
            commandList.push(command);
            let div = document.createElement("div");
            div.className = "arrow";
            div.textContent = command;
            sequenceArea.appendChild(div);
        });

        document.getElementById("play").addEventListener("click", function() {
            fetch('/execute?cmds=' + encodeURIComponent(JSON.stringify(commandList)), {
                method: "GET"
            }).then(response => response.text()).then(console.log);
        });
    </script>
</body>
</html>
"""

# Set custom HTML for the webserver
webserver._generateHTML = lambda: html

# Command execution function
def execute_commands(commands):
    for cmd in commands:
        if cmd == 'forward':
            drivetrain.set_effort(0.5, 0.5)
        elif cmd == 'backward':
            drivetrain.set_effort(-0.5, -0.5)
        elif cmd == 'left':
            drivetrain.set_effort(-0.5, 0.5)
        elif cmd == 'right':
            drivetrain.set_effort(0.5, -0.5)
        time.sleep(1)
        drivetrain.set_effort(0, 0)  # Stop after each command

# Handle requests manually
def request_handler(request):
    path = request.path
    params = request.params

    if path == "/execute" and "cmds" in params:
        try:
            commands = json.loads(params["cmds"])
            _thread.start_new_thread(execute_commands, (commands,))
            return "OK"
        except Exception as e:
            return f"Error: {str(e)}"
    
    return "Invalid Request"

# Register request handler
#webserver.add_route("/execute", request_handler, methods=["GET"])
#webserver.set_request_handler(request_handler)
webserver._catch_all = lambda path, params: request_handler(path, params)

# Logging function for debugging
def log_time_and_range():
    webserver.log_data("Time", time.time())
    webserver.log_data("Range", rangefinder.distance())
    webserver.log_data("Left Motor", left_motor.get_position())
    webserver.log_data("Right Motor", right_motor.get_position())
    webserver.log_data("Button State", board.is_button_pressed())

# Timer for logging data
timer = Timer(-1)
timer.init(freq=2, mode=Timer.PERIODIC, callback=lambda t: log_time_and_range())

# Start network and webserver
def start_network_and_webserver():
    webserver.start_network()
    webserver.start_server()

start_network_and_webserver()

