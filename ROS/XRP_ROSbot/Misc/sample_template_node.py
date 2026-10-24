#!/usr/bin/env python3
import rclpy #python lib for ROS
from rclpy.node import Node #import node class

class mynode(Node): #mynode inherit from Node class
    def __init__(self): #constructer
        super().__init__("first_node") #node name
        self.get_logger().info("Hello World!")


def main(args=None):
    rclpy.init(args=args) #initialise ros2 communications
                                 #args=args ==> args is from main    
    node = mynode()             
    rclpy.spin(node) #stop node from exiting after single execution
    
    rclpy.shutdown()

if __name__ == '__main__': #Also to directly run .py file from terminal
    main()
