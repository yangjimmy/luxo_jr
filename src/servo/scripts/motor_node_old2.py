#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point as msg_Point
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from dynamixel_sdk_custom_interfaces.srv import GetPosition

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
        self.publisher_ = self.create_publisher(SetPosition, 'set_position', 10)
        self.CurrentPosClient = self.create_client(GetPosition, 'get_position')
        timer_ts = 0.5
        self.position = 0.3
        self.timer = self.create_timer(timer_ts, self.timer_callback)
        self.MotorIDs = [1,2,3,4,5,6]
        self.MotorZeroPos = [3.14, 3.14, 3.14, 3.14, 3.14, 3.14]
        self.CurrentMotorPosTemp = 0
        self.CurrentMotorPos = self.MotorZeroPos
        while not self.CurrentPosClient.wait_for_service(timeout_sec = 1.0):
            self.get_logger().info('Waiting for get_position service')
        
    def hand_loc_received_callback(self, msg):
        """
        Updates the center location of the hand from 2D image
        self: MotorNode
        msg: message (Array.Array)
        returns: None
        """
        x,y,z = msg.x, msg.y, msg.z
        pass
        
    def timer_callback(self):
        self.position = self.position + 0.1
        #self.MotorGoInRad(2, self.position)
        #self.CommandMotor(3, 1000)
        CommandingMotors = [1,1,1,1,1,0] # Driving Motor 1 and 2: put one for motor you want to command, put zero for the others
        TargetPos = [2,-2,2.8,-2.4,1.5,0] # in rad  # Leave zero for the motors not being commanded
        #self.AllMotorsGo(CommandingMotors, TargetPos)
        #Temp = self.MotorPosReadInRad(1)
        #Temp = self.GetMotorPositions()
        self.get_logger().info(f'Current Pos:{self.GetMotorPositions([1,2,3])}')
        #self.GetMotorPositions()
        #self.get_logger().info(f'Current Pos:{Temp}')
    def GetMotorPositions(self, motor_ids):
        futures = []
        for mid in motor_ids:
            req = GetPosition.Request()
            req.id = mid
            future = self.CurrentPosClient.call_async(req)
            futures.append((mid,future))
        results = {}
        for mid, future in futures:
            rclpy.spin_until_future_complete(self,future)
            results[mid] = future.result().position
        return results
    def PositionReadingDoneCallback1(self, future1):
        try:
            response = future1.result()
        except Exception as e:
            self.get_logger().error(f"Failed to call service for motor position") 
        self.CurrentMotorPos[0] = response.position*np.pi/2048 - self.MotorZeroPos[0]
    def CommandMotor(self, motor_id, CmdPos):
        Motor_msg = SetPosition()
        Motor_msg.id = motor_id
        Motor_msg.position = CmdPos
        self.publisher_.publish(Motor_msg)
        self.get_logger().info(f'Publishing: ID={Motor_msg.id}, position = {Motor_msg.position}')
    def MotorGoInRad(self, MotorID, TargetPositionInRad):
        TargetPosition = int((TargetPositionInRad+self.MotorZeroPos[MotorID-1])*2048/np.pi)
        Motor_msg = SetPosition()
        Motor_msg.id = MotorID
        Motor_msg.position = TargetPosition
        self.publisher_.publish(Motor_msg)
        #self.get_logger().info(f'Publishing: ID={Motor_msg.id}, position = {Motor_msg.position}')
    def MotorPosReadInRad(self, MotorID):
        self.GetMotorPositions()
        MotorPos = self.CurrentMotorPos[MotorID-1]
        return MotorPos*np.pi/2048 - self.MotorZeroPos[MotorID-1]
    def AllMotorsGo(self, IDarrayToGo, motorTargetPos):
        FeedbackPos = np.zeros(6)
        for k in range(6):
            if IDarrayToGo[k] == 1:
                self.MotorGoInRad(self.MotorIDs[k], motorTargetPos[k])
                #FeedbackPos[k] = self.MotorPosReadInRad(self.MotorIDs[k])
        return FeedbackPos
        #return motorTargetPos
    def PrintMotorsPosition(self):
        
        pass
    
def main(args=None):

    """
    The main function.
    :param args: Not used directly by the user, but used by ROS2 to configure
    certain aspects of the Node.
    """
    try:
        rclpy.init(args=args)
        motor_node = MotorNode()
        rclpy.spin(motor_node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
