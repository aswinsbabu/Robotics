import serial
import time 

# Adjust the port as needed; make sure to check the correct port for your setup
s = serial.Serial(port="/dev/ttyACM0", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
message='Backward\n'

def send_msg(data):
    s.flush()  # Flush the input and output buffers
    
    # Send a test command
    #s.write(b"Forward\n")  # Ensure correct newline termination for compatibility
    s.write(data.encode('utf-8'))
    print("Send data to XRP:", data)
    # Read response from Pico, adjusting the read length as needed
    #ret_mes = s.read_until(b'\n').strip()  
    return None
    
    
def main():    
    while True:
        response = send_msg(message)
        time.sleep(0.5)
        #print(response.decode())  # Decode and print the response

if __name__ == "__main__":
    main()
