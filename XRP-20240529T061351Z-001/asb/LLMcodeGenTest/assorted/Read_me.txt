https://docs.google.com/spreadsheets/d/1YXqm057OnEYNjvmOLucvbqL6f-2cxKV4X--3lMqBr_o/edit?gid=1655658999#gid=1655658999 

I tried to generate code for XRP to perform simple task of forward and backward movement. There were 2 different scenarios tried.
1. Only the name 'XRP' was given
  Input:                                                             
"Query 1: What is XRP robot?                          
Query2: Can you write code for an xrp robot to move it forward and backward?                      
2. Harware description of XRP was given"
 Input: 
"I have a Raspberry Pi Pico W (RP 2040) based 2 wheeled robot. 
The following are the robot details. The motor driver used for controlling the motors is DRV8835 H-Bridge, 
there are 2 DRV8835 which allows for 4 motors to be controlled. 
However we are only using 2 motors now(Motor L and Motor R. 
Motors are with encoders and the GPIO connections to the motor are as follows

Motor GPIO connections
Left Motor 
GPIO4        Motor L        Left Motor Encoder A
GPIO5        Motor L        Left Motor Encoder B
GPIO6        Motor L        Left Motor Phase Pin
GPIO7        Motor L        Left Motor Enable Pin

Right Motor
GPIO12        Motor R        Right Motor Encoder A
GPIO13        Motor R        Right Motor Encoder B
GPIO14        Motor R        Right Motor Phase Pin
GPIO15        Motor R        Right Motor Enable Pin

Generate a Micro python code assuming there is no libraries used, write the entire code from scratch. This generated code should move the XRP forward and Backward. 
"
