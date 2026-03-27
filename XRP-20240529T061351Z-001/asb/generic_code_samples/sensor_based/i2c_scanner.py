#Code to scan qwiik pins(GPIO 18 & 19) on XRP board 
from XRPLib.defaults import *
from machine import Pin, I2C

i2c = I2C(0, scl=Pin(25), sda=Pin(24))  #sda=24/scl=25 for qwiik pins(GPIO 19 and 18 respectively)

print(i2c.scan())
