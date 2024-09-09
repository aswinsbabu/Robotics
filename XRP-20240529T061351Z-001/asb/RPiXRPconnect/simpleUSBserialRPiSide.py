#Pico
import sys
import machine

while True:
    # read a command from the host
    #serialMsg= sys.stdin.readline().strip()
    serialMsg= sys.stdin.readline().strip()
    print('Serial Message: ', serialMsg)
