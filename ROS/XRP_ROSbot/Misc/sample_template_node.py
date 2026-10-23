#!/usr/bin/env python3
import rclpy
from rclpy.node import Node #import node class

class mynode(Node): #mynode inherit from Node class
    def __init__(self): #constructer
        super().__init__("first_node") #node name
        self.get_logger().info("Hello World!")


def main(args=None):
    rclpy.init(args=args)
    node = mynode()


    rclpy.shutdown

if __name__ == '__main__':
    main()