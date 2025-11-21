#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point as msg_Point

import numpy as np
import os

# Outline:
# Receive hand location message
# Calculate inverse kinematics
# Send joint positions as motor commands to motor

class MotorNode(Node):
    def __init__(self):
        super().__init__('MotorNode')
        self.hand_location_subscriber = self.create_subscription(msg_Point, '/camera/camera/hand_loc', self.hand_loc_received_callback, 10)
    
    def hand_loc_recieved_callback(self, msg):
        """
        Updates the center location of the hand from 2D image
        self: MotorNode
        msg: message (Array.Array)
        returns: None
        """
        x,y,z = msg.x, msg.y, msg.z
        pass

    
def main(args=None):

    """
    The main function.
    :param args: Not used directly by the user, but used by ROS2 to configure
    certain aspects of the Node.
    """
    try:
        rclpy.init(args=args)
        predict_node = MotorNode()
        rclpy.spin(motor_node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
