#flask server 
#Joystick, USB serial
#Raspberry Pi
import serial
import time

# open a serial connection
s = serial.Serial("/dev/ttyACM0", 115200)

# blink the led
while True:
    s.write(b"F\n")
    time.sleep(1)
    s.write(b"B\n")
    time.sleep(1)
